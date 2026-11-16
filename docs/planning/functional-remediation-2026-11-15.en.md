# Product-Agent OS — functional improvements after V3

Source status: repository_source / current_local_synthetic_implementation; remaining_tasks_planned.
Planning date: 15.11.2026. Timezone: Europe/Moscow. Schema version: task_matrix_plan_v1.

<!-- func-g01-g06-status -->
FUNC-G01: 7/7 locally_verified; FUNC-G02: 3/3 poc_research_locally_verified; FUNC-G03: 7/7 locally_verified; FUNC-G04: 5/5 implemented, locally_verified_with_measured_limits; FUNC-G05: 5/5 locally_verified_with_explicit_limits; FUNC-G06:3/3 locally_verified_with_explicit_limits; overall30 implemented /4 planned. Three M5 references preserved.

## Scope and status

The plan contains **34 tasks PAOS-FUNC-01–PAOS-FUNC-34** and references to **3 previously planned M5 tasks**. Current total: **30 implemented / 4 planned**; FUNC-G01 is closed against its local technical AC. The overview matrix therefore contains 37 entries; this is not the total number of project tasks. The existing 56 M1–M5 cards, their 53 implemented / 3 planned statuses, and estimates are preserved. New findings do not rewrite historical receipts: they require current reproduction and a new verification.

Machine-state owner for the current checkout: `docs/planning/functional-remediation-2026-11-15.json`. The [original planning snapshot](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/functional-remediation-2026-11-15.json) is historical and does not carry the updated local statuses. This Markdown file owns technical and product rationale, acceptance and completion evidence. M5 references do not create a second owner for status: the owners are [docs/planning/product-agent-os-web-task-manager-task-group-2026-11-09.json](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/product-agent-os-web-task-manager-task-group-2026-11-09.json) and [docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md](product-agent-os-web-task-manager-plan-2026-11-09.md).

The original request authorized planning. A subsequent 2026-11-15 owner request authorized complete FUNC-G01 implementation, necessary local synthetic checks, statuses and documentation; all seven group tasks are implemented. A further owner request authorized FUNC-G02: its three research PoCs are closed with measured decisions and isolated UI acceptance. Further requests authorized G03 (7 implemented) and G04 (5 implemented with measured limits); G05 is now implemented (five tasks); G06 is implemented (three tasks); four FUNC tasks and the separate M5 references remain planned. P1 means an execution blocker or an integrity/recovery check; P2 means functional value, information correctness and maintainability; P3 means a limited display defect. The priority of a verification task does not mean a failure has already been observed.

## Original evidence basis and limits

- The 15.11.2026 static source audit identified seven candidate defects F01–F07. F01 is supported by a fingerprint comparison: current `apps/web/package-lock.json` SHA-256 `f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac`, qualified `d279009aa1dca2bd2d6ba0e18a77d085a67e872d0dce78dd360fb23d43975f38`; native broker failure is inferred from the contract check and must be reproduced. Runtime was not run during this planning.
- F08–F10/F18/F24 concern implementation structure and completeness of the user journey. Performance is not considered poor without measurements: F20 precedes F09.
- F11–F17 are missing extensions or deliberately limited capabilities of the current local scope. They are not seven proven redesign regressions. Before build, available capabilities and decisions about data, writes, privacy or distribution channel are needed.
- F19–F23 concern missing current evidence. Historical Web/browser receipts in [design/2026-11-13-v3/implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md) are not presented as newly executed checks.
- The previous audit Markdown was not created because its write was denied; primary references and observations were transferred to each card's Source. The chat and this plan do not replace code and current runtime results.
- This plan makes no claims about external APIs or OpenAI capabilities. If a task relies on a new host/provider contract, discovery must check current official documentation and the interface actually available.

## Recommended sequence

1. F01/core fixes and F28 retain their branches. F30/F31/F32 are independent PoCs on synthetic fixtures: first a shared protocol, versions and UI wireframes, then measurements. They do not wait for implementation of F28/F27/F20; they use agreed draft contracts and one baseline protocol. The current request does not start PoCs.
2. F28 → F26/F27 → F29. The file browser is available before the graph/database and does not depend on F30–F34. Shared HTTP/API/storage/UI files are changed in sequential slices with explicit ownership. F18 defines the freshness contract; new consumers implement it in their tasks.
3. F20 preserves a baseline and checks already implemented files/scan/discovery. F20 → F09; F14 uses F09/F27/F28 and decisions from both F30/F31. A justified reject completes a PoC, but downstream build requires an alternative or an explicit blocker.
4. F32 + F26/F27/F28 → F33 (DB schema and a complete UI section); F14 + F33 → F34 (code-to-table links and usage/impact UI). New adapters repeat the F20 benchmark protocol in their AC; F20 does not depend on F14/F33/F34 and there is no cycle.
5. F24 finalizes capabilities for all new screens after F14/F33/F34; early Files/scan states are implemented without waiting. F19 accepts the full Files → Map → Database → code usages → source journey; early Files receipts remain separate. F23 then checks human understanding and usefulness. F25 synchronizes claims as features are implemented.
6. M5 remains a separate track: PAOS-0047 is optional, PAOS-0052 → PAOS-0053 does not depend on sign-in. F33 does not implement team storage or automatically open external databases.

Hard dependencies are recorded in Depends on/JSON; Blocks are exact reverse edges; execution_order is a valid topological sequence, not authorization for parallel writes. F30/F31 do not require integration of both engines: F14 records one backend or an explicit composition. Full acceptance and the human pilot await integration of the new UI; early Files functionality does not wait for it.

Estimates are preliminary: F30–F32 include PoCs and isolated UI prototypes, not production integration. F33/F34 estimate design; build follows adapter selection and UI review. No overall completion date is inferred; F23 retains 14 days of observation.

## Delivery groups — 7 agreed subgroups

Source status: repository_owned_plan_dependency_analysis; planning_only. The 15.11.2026 grouping covers **all 34 PAOS-FUNC tasks exactly once**. These are delivery layers over the original cards: IDs, acceptance, Depends on/Blocks, execution_order, estimates and statuses are preserved. Three M5 references remain in the external source-owned plan and are not included in these seven groups. Membership and cross-group edges are mirrored in JSON (`delivery_groups`, `delivery_group_id`); status belongs to the task, not a separate group-status copy.

### Executing groups without unnecessary waiting

The groups are not seven sequential large releases. `depends_on_groups` means edges exist between individual tasks; a ready task can start without waiting for every member of the previous group. Internal branches below are convenient slices; always read additional prerequisites in the original card. Overlapping work locations restrict simultaneous writes; they do not add a functional dependency.

| Group | Result | Tasks | External task dependencies from groups |
| --- | --- | --- | --- |
| FUNC-G01 — Stability of the current UI and core contracts | Confirmed UX defects fixed, native runtime qualified, UI/backend contracts have independent ownership. | F01, F03, F04, F05, F06, F07, F08 | None |
| FUNC-G02 — Selection of existing engines and UX prototypes | Measured adopt/bounded_adopt/reject decisions and code/DB adapters; verified isolated UX prototypes. | F30, F31, F32 | None |
| FUNC-G03 — Files, scanning and project onboarding | The project folder is immediately available; scanning is controllable, discovery and file references are consistent, changes and limitations are visible. | F28, F26, F27, F02, F29, F10, F18 | FUNC-G01 |
| FUNC-G04 — Performance, code map and database | Measured performance, code graph, ERD/schema diff and explainable code-to-table links are available to the UI and agent. | F20, F09, F14, F33, F34 | FUNC-G01, FUNC-G02, FUNC-G03 |
| FUNC-G05 — Agent capabilities, documents and control | Reliable metrics and history, skills search, safe application of proposals and enforceable autonomy. | F11, F12, F13, F15, F16 | FUNC-G01, FUNC-G03 |
| FUNC-G06 — Data recovery and application delivery | Stop/crash/import/backup/restore are checked and safe install/update/rollback prepared for the selected channel. | F21, F22, F17 | FUNC-G01 |
| FUNC-G07 — End-to-end acceptance, UI clarity and documentation | Capabilities are consistent in the UI, the full user journey is checked, and the human pilot and documentation have accurate statuses. | F24, F19, F23, F25 | FUNC-G01, FUNC-G03, FUNC-G04, FUNC-G06 |

### FUNC-G01 — Stability of the current UI and core contracts

- **F01** — Restore native runtime qualification after the redesign.
- **F03** — Fully reset the new-task draft.
- **F04** — Preserve workflow assignment drafts during navigation.
- **F05** — Show incomplete portfolio coverage next to totals.
- **F06** — Correct dashboard queue numbering.
- **F07** — Sort recent tasks by time.
- **F08** — Separate shared contracts and UI/backend dependencies.

- Result: Confirmed UX defects fixed, native runtime qualified, UI/backend contracts have independent ownership.
- Entry conditions: F01/F03–F07 have no task dependencies; F08 only after F01 and architecture review.
- Internal branches: F01 → F08; F03; F04; F05 → F06 → F07. Independent branches do not authorize overlapping writes.
- Combined work for speed: Editor and WorkflowManager can be checked separately from runtime; combine F05/F06/F07 under one Dashboard/model owner and one regression set.
- Ownership: Runtime/manifest; task Editor; WorkflowManager; Dashboard/model; contracts. One writer per area; coordinate F08 application.mts with G03.
- UI/UX: Existing forms and dashboard: state preservation/reset, sorting/numbering and honest coverage labels.
- Exit condition: All seven cards meet their own AC; runtime tuple is confirmed on the checked version and reset/navigation/dashboard regressions are checked. UI fixes do not wait for PoC.

### FUNC-G02 — Selection of existing engines and UX prototypes

- **F30** — Evaluate dependency-cruiser for a JS/TS dependency graph.
- **F31** — Evaluate codebase-memory-mcp as an indexing engine for agents.
- **F32** — Evaluate tbls for DB schema extraction and Mermaid ERD.

- Result: Measured adopt/bounded_adopt/reject decisions and code/DB adapters; verified isolated UX prototypes.
- Entry conditions: No hard dependencies. First agree on the protocol/ground truth, pinned versions/licenses and draft F28/F20 contracts; completed F28/F20 implementations are not needed.
- Internal branches: F30; F31; F32. Independent branches do not authorize overlapping writes.
- Combined work for speed: Three independent PoCs on agreed fixtures; compare F30/F31 on identical tasks. One owner integrates findings into shared architecture/design/matrix.
- Ownership: Separate disposable PoC roots/processes and evidence; shared prototype navigation/data contract, one design/architecture integrator.
- UI/UX: Map and Database prototypes, graph/list/Mermaid, evidence, coverage and failure states; not production UI.
- Exit condition: Each PoC ends with a decision, evidence and limitations; F14/F33 select a suitable backend. Reject does not mean a feature is implemented and does not authorize silent fallback.

### FUNC-G03 — Files, scanning and project onboarding

- **F28** — Unify inventory, coverage and exclusions.
- **F26** — Add a project file browser.
- **F27** — Make scanning a managed background job.
- **F02** — Restore links between structured artifacts and tasks.
- **F29** — Connect core discovery to project onboarding.
- **F10** — Show file-scope limitations before execution.
- **F18** — Align refresh of task and dashboard snapshots.

- Result: The project folder is immediately available; scanning is controllable, discovery and file references are consistent, changes and limitations are visible.
- Entry conditions: F28 is independent; F26/F27/F02 follow F28. F10 also requires F01, F18 requires F05/F07. Do not wait for all of G01 or G02.
- Internal branches: F28; F26 → F10; F27 → F29; F02; F18. Independent branches do not authorize overlapping writes.
- Combined work for speed: After the inventory contract, prepare directory and scan adapters separately, but wire application.mts/api/client.ts sequentially. F29 follows F27; tie reader/scope/freshness to the same paths/revisions.
- Ownership: One inventory/root-policy owner; sequential shared HTTP/API/storage patches; Files/Onboarding/freshness UI with shared navigation.
- UI/UX: Files section, reader, project overview/scan progress, scope preflight, stale/error/unsupported and return after restart.
- Exit condition: All seven cards meet their AC; Add→Files→scan→discovery→file reference passes, cancel/restart/retry and root boundaries are checked. Files works without G04.

### FUNC-G04 — Performance, code map and database

- **F20** — Measure scaling and long-running behavior.
- **F09** — Optimize snapshot reads and lifecycle.
- **F14** — Improve usefulness and resilience of the project map.
- **F33** — Add a DB map and the project Database section.
- **F34** — Link code to tables and show change impact.

- Result: Measured performance, code graph, ERD/schema diff and explainable code-to-table links are available to the UI and agent.
- Entry conditions: F20 after F01/F26/F27/F29; F09 after F08/F20; F14 after F02/F09/F27/F28/F30/F31. F33 after F26/F27/F28/F32 and may start before F20/F09/F14. F34 waits for F14 and F33.
- Internal branches: F20 → F09 → F14; F33; F34. Independent branches do not authorize overlapping writes.
- Combined work for speed: After input contracts, run code and DB branches independently; shared SQLite/schema/scans/API/UI wiring has one writer. F34 combines completed outputs. Measurement before optimization remains mandatory.
- Ownership: Code-index/impact; database-map; storage/scans; GraphExplorer/DatabaseExplorer. Integrate shared App/Sidebar/client/locales and schema migrations in sequential slices.
- UI/UX: Map: dependencies/symbols/impact; Database: Schema, Changes, Code usage; bidirectional source-line navigation and accessible list/table.
- Exit condition: Five cards meet AC and budgets; compatible revisions/coverage/provenance are preserved, read-only DB is demonstrated, graph/table/Mermaid are consistent. The new workload is repeated in F14/F33/F34 without reversing the F20 dependency.

### FUNC-G05 — Agent capabilities, documents and control

- **F11** — Introduce measurable run and consumption statistics.
- **F12** — Design and connect external skills search.
- **F13** — Add safe application of document proposals.
- **F15** — Clarify and extend autonomy boundaries.
- **F16** — Confirm available history and actually loaded profiles.

- Result: Reliable metrics and history, skills search, safe proposal application and enforceable autonomy.
- Entry conditions: F12 design is independent; F16 follows F01; F11 follows F05/F08; F13 follows F02/F08; F15 follows F01/F10/F11. Each card's actual source/provider/write/enforcement gates remain.
- Internal branches: F11 → F15; F12; F13; F16. Independent branches do not authorize overlapping writes.
- Combined work for speed: After contracts, proposals and autonomy can be prepared separately. F11/F12/F16 share team/service.mts and TeamManager — one owner and sequential integration.
- Ownership: Team/telemetry/history; ArtifactExplorer/writer; autonomy/runtime. Coordinate shared team/service, Dashboard, artifacts/service and HTTP patches with G01/G03/G04.
- UI/UX: Dashboard/Team/History/Artifacts/Autonomy: source/version, confirmed loaded state, proposal preview/conflict, limits and reasons for unavailability.
- Exit condition: Each of five cards is supported by available sources and its own AC; unsupported remains unknown/unavailable, provider/target authority is not expanded. A design-only decision does not close an implementation task.

### FUNC-G06 — Data recovery and application delivery

- **F21** — Recheck the queue, Stop and crash recovery.
- **F22** — Recheck import, backup and restore.
- **F17** — Prepare usable installation, update and rollback.

- Result: Stop/crash/import/backup/restore are checked and safe install/update/rollback prepared for the selected channel.
- Entry conditions: F21/F22 after F01; F17 after F01/F22 and a separate distribution/signing/licensing design gate. Do not wait for G04/G05 for early synthetic checks.
- Internal branches: F21; F22 → F17. Independent branches do not authorize overlapping writes.
- Combined work for speed: Crash and data recovery can use separate disposable profiles. Packaging follows recovery evidence; shared runtime/launcher/profile resources cannot be changed simultaneously.
- Ownership: Recovery fixtures; import/export/backup; desktop-local/launcher. Disposable profiles only, no writes to a user profile or publication.
- UI/UX: Clear recovery/compatibility/update/rollback states and profile preservation; separate irreversible/external actions follow the original gates.
- Exit condition: Three cards meet their own AC; qualification applies to a specific tuple/schema/build. After significant later runtime/storage/packaging changes, repeat precisely the affected checks; an early pass does not prove the final build.

### FUNC-G07 — End-to-end acceptance, UI clarity and documentation

- **F24** — Explain capability availability at the point of action.
- **F19** — Check end-to-end functionality on the current build.
- **F23** — Conduct product acceptance for key scenarios.
- **F25** — Align current product statuses and criteria.

- Result: Capabilities are consistent in the UI, the full user journey is checked, and the human pilot and documentation have accurate statuses.
- Entry conditions: F25 runs from the first group, F24 as consumers become available; their full closure follows original AC. F19 follows its dependencies, F23 follows F19/F21/F22/F24; an early limited pilot does not close the whole backlog.
- Internal branches: F24 → F19 → F23; F25. Independent branches do not authorize overlapping writes.
- Combined work for speed: Docs and capability copy accompany feature slices; F19 may retain early Files receipts. Final F24→F19→F23 is sequential; separate human acceptance is not replaced by tests.
- Ownership: One App/Sidebar/locales/capabilities integrator; tester owns combined-build evidence; product owner owns human pilot, docs owner owns F25. No duplicate group status copies.
- UI/UX: Unified navigation for Files/Map/Database and other modules, RU/EN/themes/a11y, consistent status labels, clear next actions and the complete end-to-end journey.
- Exit condition: All four cards meet AC; closing the entire grouped backlog additionally requires G01–G06 closure, applicable G05/G06 cross-group scenarios, and final-build provenance. An open gate is not concealed by removing a task from the group; M5/release readiness is not claimed.

### Delivery order and acceleration points

1. **First work to start:** independent F01/F03/F04/F05–F07 (G01), F30–F32 (G02), F28 (G03), F12 design (G05) and current F25 docs (G07). This is a readiness plan, not a launch of agents/PoCs now. Dashboard/model F05–F07 has one owner.
2. **Early useful result:** after F28 deliver F26 tree/reader and F27 scan lifecycle; then F02/F29/F10/F18 according to their prerequisites. F08 after F01 stabilizes shared contracts; its HTTP edits and G03 wiring are sequential. Files does not wait for code engine/DB selection. F21/F22/F16 become independently available after F01.
3. **Two map branches:** F20 → F09 → F14 with F30/F31 decisions; in parallel F33 after F32/F26/F27/F28. F33 does not wait for F20/F09/F14. Then F14 + F33 → F34. This avoids waiting for the code branch while working on DB schema.
4. **Other capabilities:** F11/F12/F13/F16 by their gates, then F15 after F10/F11/F01. F17 follows F22 and the distribution decision; grouping does not authorize actual publication/installation. Shared team/API/storage wiring is sequential.
5. **End-to-end closure:** F24 → F19 → F23 after original dependencies; F25 accompanies all groups. Full G07/backlog closure requires G01–G06 and current applicable receipts, including G05 capabilities and G06 delivery/recovery. Their absence is not masked by a narrower F19 pass. M5 and broad release readiness are separate.

The dependency chain for planning is F28 → F27 → F29 → F20 → F09 → F14 → F34 → F24 → F19 → F23; nodes have additional prerequisites, such as F26 for F20, F08 for F09 and F33 for F34. This is not a calculated time critical path: design/build estimates differ and exact durations are unavailable. No acceleration percentage or deadline is claimed.

### Shared files: mandatory sequential integration

| Area | Overlapping groups/tasks | Rule |
| --- | --- | --- |
| `http/application.mts`, contracts | G01/F08, G03/F26/F27/F29, G05/F13 | Agreed API contract; one writer per shared file, integrate handlers sequentially |
| SQLite/schema/code-index/scans | G03, G04; evidence G06 | One migration/storage owner; separate adapters allowed after interface freeze, then scoped integration/recovery |
| `App.tsx`, `Sidebar.tsx`, `api/client.ts`, locales | G03, G04, G07 | One navigation/API integrator; separate feature components; do not edit router and labels concurrently |
| Dashboard/model and Team service/UI | G01/F05–F07, G03/F18, G05/F11/F12/F16, G07/F24 | Combine changes to one area in an agreed slice; do not mix totals/coverage/freshness |
| Artifacts/impact | G03/F02/F28, G04/F09/F14/F34, G05/F13 | First unified paths/revisions, then readers/graph and a separately approved writer contract |
| Architecture/design/matrix/docs | G02, G04, G05, G07/F25 | One owner of the final document; independent results do not imply concurrent writing |
| Disposable runtime/profile | G01/F01, G06/F21/F22/F17, final G07 | Separate synthetic roots and process ownership; do not destroy/update another owner's profile |
### Grouping risks and verification criteria

- F20 cannot be moved solely to final verification: it provides the basis for F09. F09 is not optimized without a reproduced bottleneck.
- F30/F31/F32 do not require completed product integration to start; a PoC decision is not equivalent to completing F14/F33.
- F21/F22 can run early, but substantial storage/runtime changes require a scoped retest on the new version; identical checks are not repeated without changed inputs.
- F24/F25 begin as delivery progresses; placing them in G07 does not defer UX/status/docs to the end. Human F23 retains a separate protocol and 14-day observation; a technical pass does not replace it.
- G05/F12/F13/F15/F16 and G06/F17 retain source/authority/enforcement/distribution gates. A group can be partially ready; an unresolved gate remains visible and is not completion.
- Before closing the grouped backlog, reconcile every task AC, UI/API/agent transitions and the final build. No member or M5 reference is lost; duplicates and task/group cycles are forbidden; shared writes must have one owner.

## Complete overview matrix of new tasks

F01 in abbreviated dependencies means PAOS-FUNC-01. Task cards and JSON own current statuses; original estimates are preserved.

| ID | Priority / type | Task | Technical value | Product value | Acceptance criteria | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| PAOS-FUNC-01 | P1 · Defect | Restore native runtime qualification after the redesign | Align lockfile, manifest and native broker without weakening the fingerprint check. | Starting a task from the redesigned UI actually results in execution. | 1) Reproduce package_lock_mismatch with the current lockfile; the fix must not substitute a simple hash overwrite for qualification.<br>2) On a newly qualified tuple, the new broker executes a synthetic command within the permitted root and rejects writes outside it.<br>3) Negative scenarios for changed binary, lockfile and adapter remain fail-closed; restart passes. | — |
| PAOS-FUNC-02 | P2 · Defect | Restore links between structured artifacts and tasks | Unify normalization of files, artifactReferences, artifacts and fileContexts. | A document can be found from its task, and a task from the document and search. | 1) A task referenced only in artifacts.reference is found by the catalog taskId filter and displayed among the document's linked tasks.<br>2) Legacy artifactReferences/files preserve behavior; duplicates and path separators are normalized.<br>3) External URLs are not treated as local paths; stale revision and unavailable file are shown explicitly.<br>4) File references use F28 normalization and root identity; catalog, tree and tasks point to the same permitted relativePath/revision. Deleted/moved/excluded does not become an accessible document or read permission. | F28 |
| PAOS-FUNC-03 | P2 · Defect | Fully reset the new-task draft | Synchronize model, rawInputs, estimate, preview and dirty-state on Discard. | After cancellation, the user does not see data already absent from the saved task. | 1) Populate criteria/risks/references/estimate in a new task and press Discard: all fields and model return to the same empty state.<br>2) The next save does not restore discarded data; dirty/preview/error states are not misleading.<br>3) For an existing task, Discard restores the server revision and does not destroy another user's changes. | — |
| PAOS-FUNC-04 | P2 · Defect | Preserve workflow assignment drafts during navigation | Include typeMapping and original CAS revision in the shared draft lifecycle. | The user does not lose unsaved process assignments when navigating between sections. | 1) Change task-type mapping, leave Settings and return: the draft is restored or navigation is stopped beforehand with a clear choice.<br>2) Save/Discard correctly clear dirty-state; default workflow and mapping do not overwrite each other.<br>3) Switching projects does not transfer the draft into another project; a stale save returns conflict without losing the input. | — |
| PAOS-FUNC-05 | P2 · Defect | Show incomplete portfolio coverage next to totals | Pass partial/loaded/expected from the aggregator into KPI and progress displays. | Partially loaded projects do not look like a complete portfolio total. | 1) With one successful and one failed project, show “1 of 2; incomplete data” next to totals.<br>2) Unknown values are not replaced with zero; progress explicitly refers to the available sample.<br>3) Loading, retry, all-failed and restoration of full coverage are checked in RU/EN. | — |
| PAOS-FUNC-06 | P3 · Defect | Correct dashboard queue numbering | One 1-based position contract between scheduler and frontend. | Tasks have the same order on the dashboard and in queue management. | 1) Backend positions 1/2 appear as #1/#2 on the dashboard.<br>2) A null position shows no number; reorder is reflected consistently on both surfaces. | — |
| PAOS-FUNC-07 | P3 · Defect | Sort recent tasks by time | Define explicit updatedAt sorting with stable tie-breaker and unknown policy. | The recent-task block leads to genuinely recent work. | 1) UUID order is deliberately opposite to time: the 3 most recent by updatedAt are displayed.<br>2) Equal and missing timestamps are handled deterministically; the label explains the selected semantics.<br>3) Creating and changing a task updates the block after refresh. | — |
| PAOS-FUNC-08 | P2 · Architecture | Separate shared contracts and UI/backend dependencies | Remove backend→frontend and contracts→backend imports while preserving public behavior. | Appearance changes are less likely to break server functions and delivery. | 1) Preferences and task decoder have one independent owner; contracts do not import apps.<br>2) Existing payload/schema and failure scenarios are preserved; frontend and service pass typecheck and current tests.<br>3) An import-direction check prevents regression; runtime tuple is requalified if pinned sources are affected. | F01 |
| PAOS-FUNC-09 | P2 · Architecture | Optimize snapshot reads and lifecycle | Eliminate measured redundant full scans and add bounded cache release. | Long-running work and large projects are not hindered by delays and accumulated snapshots. | 1) Select and implement only bottlenecks reproduced by F20; before/after uses the same workload.<br>2) The ninth project does not require restart solely due to 8 graph snapshots: eviction/rebuild preserves revision/cursor safety.<br>3) Task/artifact/history read load is bounded; exceeding budget yields explainable partial/error and safe recovery.<br>4) After F20 compare metadata listing, graph status and scanner on the same workload: a repeated status query must not unconditionally reread all file contents; bytes/read and scan count are measured.<br>5) Cache key/eviction accounts for root identity, policy version and F27/F28 scan revision; eviction does not hide files from the F26 tree or mix projects. | F08, F20 |
| PAOS-FUNC-10 | P2 · Improvement | Show file-scope limitations before execution | Shared preflight for file count, sizes, excluded paths and actual-diff boundaries. | The user understands in advance why a task cannot start and how to split it. | 1) Check 32/33 files, 64KiB/64KiB+1 and total 512KiB before dispatch with a specific explanation.<br>2) Sensitive/link/binary exclusions do not reveal contents; blocked execution is not presented as a started run.<br>3) Any required limit increase passes a separate bounded performance/security gate; limits are not removed unconditionally.<br>4) A file reference selected from the F26 tree undergoes execution preflight again: visibility/readability/indexing does not authorize dispatch. Show F28 policy and actual execution limits separately; stale path/root requires refresh. | F01, F26, F28 |
| PAOS-FUNC-11 | P2 · Extension | Introduce measurable run and consumption statistics | Versioned telemetry with provenance, deduplication and session→run→task→agent aggregation. | Duration and consumption help compare work without invented numbers. | 1) First approve available duration/tokens/tool calls/cost sources, privacy and retention; unsupported fields remain unknown.<br>2) Event replay does not increase totals; partial streams, restart and links to multiple agents do not cause double counting.<br>3) Dashboard, task and agent show consistent values, period and source; cost appears only with a known calculation model. | F05, F08 |
| PAOS-FUNC-12 | P2 · Extension | Design and connect external skills search | Separate read-only discovery adapter with provenance, license, pin and preview. | A suitable skill can be found outside the local catalog and added with an informed decision. | 1) Before build choose a permitted source, network/privacy policy and result format.<br>2) Search shows origin/license/revision; timeout/offline does not break the local catalog.<br>3) Search installs nothing; adding uses existing preview/apply and checks drift and dependencies. | — |
| PAOS-FUNC-13 | P2 · Extension | Add safe application of document proposals | Preview-bound compare-and-swap writer preserving user changes and recovery. | An agreed proposal can be applied to a document within the app. | 1) Before build approve writer authority, source-vs-SQL ownership and eligible documents.<br>2) Apply changes only the checked file when revision matches; an external edit causes conflict without overwrite.<br>3) Repeated apply is idempotent; crash/rollback and sensitive paths are tested; staged/applied/accepted are shown separately. | F02, F08 |
| PAOS-FUNC-14 | P2 · Extension | Improve usefulness and resilience of the project map | Choose language/relation support; durable revision index, imports resolution and honest coverage. | The map helps assess change impact without giving the appearance of complete analysis. | 1) Before build approve supported language/relation-type matrix; unsupported semantics remain explicitly marked.<br>2) Within selected scope test cross-file imports/aliases on ground-truth fixtures; unresolved does not become a false edge.<br>3) Restart/rebuild preserves or explicitly invalidates revision; D3/Mermaid/list and impact show one data set.<br>4) The graph consumer uses F28 inventory and F27 code stage; discovered/readable/indexed/unsupported/excluded/error are distinct. An empty or successful JS/TS index does not imply complete project analysis.<br>5) Graph ready/stale/unavailable does not block the F26 tree; restart/cancel/retry do not publish stale results, an unavailable parser leaves other scan results accessible.<br>6) Record backend/composition and rollback selection from F30/F31; a justified PoC rejection is not a hidden fallback. Unsupported languages and semantics are explicit; a third-party engine's raw SQLite does not become the PAOS API.<br>7) In the existing Map implement dependency/symbol modes within selected capabilities, search, incoming/outgoing, path/impact and an evidence drawer with file/line navigation. Graph/list/Mermaid, filters and counters use one snapshot; loading/empty/partial/error/unavailable/stale and version/coverage are visible.<br>8) Apply the shared F30–F34 UI/UX contract to the production screen, not only the PoC; test Files↔Map navigation and project selection. Architecture is included only for a source-backed model: import is not a call, and C4 grouping is not an extracted business fact. | F02, F09, F27, F28, F30, F31 |
| PAOS-FUNC-15 | P2 · Extension | Clarify and extend autonomy boundaries | Capability-based file/operation/cost policy without promising control over the entire App host. | The user understands and controls permitted agent autonomy. | 1) Before build document enforceable boundaries and impossible promises; reject narrow-path execution without enforcement.<br>2) In the permitted route, exceeding scope/limit stops new dispatch; unknown outcome remains fenced.<br>3) A monetary limit is allowed only with sufficient F11 metering/reservation; otherwise the UI clearly reports unavailability. | F01, F10, F11 |
| PAOS-FUNC-16 | P2 · Extension | Confirm available history and actually loaded profiles | Separate configured/pinned/observed model, effort and asset version; capability-based history adapter. | The user knows which agent actually ran and what history is available. | 1) Before build verify the supported host contract; inaccessible history is not retrieved by bypassing private stores.<br>2) UI distinguishes configured/pinned/observed; loadedVersion appears only from a confirmed event.<br>3) Reconnect/profile switch do not mix history and identity; explain partial coverage and missing attestation. | F01 |
| PAOS-FUNC-17 | P2 · Extension | Prepare usable installation, update and rollback | Define version/digest/signing, compatibility and recovery UX on top of the portable package. | Updates do not require manual directory selection or endanger data. | 1) Before build choose distribution channel, installer format, signing and AUTH/licensing gates; publication is separate.<br>2) Synthetic install/update/rollback preserve the profile; incompatible schema/tuple blocks startup with clear recovery.<br>3) User profiles and older versions are not removed without a separate decision; a new clean Windows profile passes the agreed scenario. | F01, F22 |
| PAOS-FUNC-18 | P2 · Improvement | Align task and dashboard snapshot refresh | Define refresh/invalidation contract for background work, mutations and project switches. | After execution the user sees current status without guessing which screen to refresh. | 1) A task/queue change through another permitted channel either refreshes the screen or explicitly marks the snapshot stale.<br>2) A late response from the previous project does not replace current data; refresh does not overwrite a dirty editor.<br>3) Polling/subscription stop on unmount and do not create unbounded load.<br>4) Create/modify/rename/delete and policy/root changes invalidate affected directory/document/graph/analysis snapshots; choose a watcher or bounded rescan/refresh with explicit freshness, without promising an unselected live watcher.<br>5) Scan events include scanId/revision; late events from a cancelled job or another project do not change the UI. After return/restart show the retained scan status without overwriting drafts.<br>6) The common freshness contract covers code/schema snapshots and code-table links: compatible revisions, late-response rejection, explicit stale and stopping polling on exit. F14/F33/F34 implement and test new consumers; F18 does not wait for them or block the early Files path. | F05, F07, F26, F27 |
| PAOS-FUNC-19 | P1 · Verification | Check end-to-end functionality on the current build | Link real UI/API/storage/native receipts to one revision without substituting mock execution data. | The user completes the entire working journey and receives a verifiable result. | 1) The synthetic task→assignment→run→approval→command→diff/checks→owner acceptance path passes on the current build.<br>2) Forms, custom workflow, RU/EN, both themes, keyboard, links and partial/error states are checked after F02–F07/F10/F18.<br>3) Actual App/model roundtrip and agent/skill generation are tested only with separate authorization; without it record the live gap, which a synthetic pass does not close.<br>4) On a synthetic fixture test Add → immediately available tree → scan stages → allowed file preview → task file reference; map and discovery do not substitute for complete file-tree coverage.<br>5) Test empty/no-Control-plane/Python-only/mixed projects, Unicode/spaces, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift during scan, cancel/restart/retry and two projects. An individual file failure preserves the allowed portion, root violations are blocked; before/after target hashes match.<br>6) Verify RU/EN, two themes, keyboard/focus, pagination, explicit incomplete search and absence of false-ready; fixtures use no real profiles/credentials and execute no target scripts.<br>7) After F14/F33/F34 test the expanded Files → Map → DB schema → code usages → source line → task reference journey; preserve selection/back/filter/project isolation. Verify confirmed/inferred/unresolved, runtime schema vs ORM/migrations, Mermaid export and bounded large graphs.<br>8) New tabs/sections have RU/EN, both themes, keyboard/focus, accessible list/table fallback and all UI states; backend failure/cancel/restart are not masked by mock UI. Separate early Files/scan receipts are allowed before graph/DB, but final F19 closure requires the expanded scenario. | F01, F02, F03, F04, F05, F06, F07, F10, F18, F24, F26, F27, F29, F14, F33, F34 |
| PAOS-FUNC-20 | P2 · Verification | Measure scaling and long-running behavior | Reproducible workload with hardware/cache profile, latency/RSS/queue-depth and error budgets. | Large projects and long sessions remain manageable. | 1) Record hardware/cache and volumes: 10k tasks, 100k messages, 1k files; separately check boundaries of 1001 files and 9 projects.<br>2) Measure cold startup, search/list/event-visible latency, RSS and snapshots in a repeatable long run; no hidden data loss.<br>3) Compare results against WEB-NFR and agreed thresholds; record deviations under F09 and explicitly limit unsupported volumes.<br>4) Fix budgets and dataset before measurement: large monorepo, wide/deep directory, empty folders, generated/vendor/ignored, binary/large, mixed languages. Measure registration-to-tree, expansion/search, scan phases, cancellation latency, restart recovery, RSS, traversal count and bytes read.<br>5) Test legacy limits 1000/1001 files, 10000/10001 entries, depth 32/33, 512KiB and 8MiB as correct partial/bounded outcomes, not a demand to remove guards. Metadata listing need not read all project contents.<br>6) Baseline can precede F26–F29; final F20 closure requires their version and comparison with baseline. F09 uses this protocol for before/after; the benchmark does not modify the user workspace.<br>7) One reproducible benchmark protocol sets ground truth and budgets for F30/F31/F32: cold/incremental scan, RSS/disk, latency and precision/recall. F14/F33/F34 add UI responsiveness, schema size, edge limits and bounded agent-context cost; they repeat the protocol in their own AC. F20 does not depend on completion of PoC/DB/graph, avoiding an F20→F09→F14 cycle. | F01, F26, F27, F29 |
| PAOS-FUNC-21 | P1 · Verification | Recheck queue, Stop and crash recovery | Check identity/CAS/lease/ownership fences and absence of replay in failures. | Connection loss neither starts a task twice nor loses the result. | 1) Cover crash before dispatch, after dispatch before receipt, and after terminal receipt as separate scenarios.<br>2) Stop without ACK does not release ownership; lost consumer/timeout require proper reconciliation.<br>3) Allowed parallelism remains across different roots, overlapping roots are blocked; selective Stop does not cancel another run. | F01 |
| PAOS-FUNC-22 | P1 · Verification | Recheck import, backup and restore | Check source authority, freeze/CAS, counts/hashes/FK, blobs and idempotency. | Tasks, history and attachments survive migration and recovery. | 1) Source drift and unknown writer stop cutover; two writable authorities never arise.<br>2) Corrupt/missing blob, interrupted import and request replay yield safe results without duplicates.<br>3) Restore into a new synthetic profile preserves data and links; old profile is unchanged; credentials/pending operations are not replayed. | F01 |
| PAOS-FUNC-23 | P2 · Verification | Conduct product acceptance of key scenarios | Tie acceptance to observable correctness of decisions, not number of clicks. | The user understands status, blocker, evidence and next action without prompting. | 1) Before the pilot agree participants, scenarios, opt-in/retention and MD/chat baseline; production data is not required.<br>2) Cover first opening, return, conflict, partial evidence and acceptance; document comprehension errors alongside successes.<br>3) Test PRD goals of 4/5 in 3 minutes and 3/5 reuse in 14 days as hypotheses; zero false interpretations of verified and data loss; owner accepts results separately.<br>4) Add folder selection, finding an ordinary file outside Control-plane, explaining excluded/unsupported/partial, cancel/retry and return after restart. Observer checks that the participant does not confuse file visibility, successful indexing and execution authorization.<br>5) Human pilot includes finding a change location via Map and DB usages, reading ERD/table, navigating to source, understanding stale/partial/inferred and discovering unsupported semantics. Compare success and time with the agreed baseline; UI convenience is not inferred from technical tests. | F19, F21, F22, F24 |
| PAOS-FUNC-24 | P2 · Improvement | Explain capability availability at the point of action | Unified capability vocabulary for staged/unsupported/partial/connected/qualified/accepted. | The user distinguishes an available capability from a screen offering a future one. | 1) For usage, graph, proposals, skills discovery, history, autonomy and runtime, show actual scope and reason for unavailability next to the action.<br>2) Provide a concrete next step; unsupported does not look like loading, connected is not called execution-qualified.<br>3) RU/EN and accessibility states are checked; no repeated request for already valid bounded authority.<br>4) Onboarding and project show independent registration/tree/inventory/documents/code/analysis states from F26–F29, observation time and scope; counts.files is not called indexed without corresponding coverage.<br>5) Empty/no-supported-code does not get a false “project fully analyzed”; excluded/error/unsupported explain reason and action. An unavailable parser/core adapter does not hide the available tree; the Control-plane checklist is explicitly named as a separate filter.<br>6) Project navigation and onboarding clearly distinguish Files, Map, DB schema and code usages; Settings owns registration/source and does not duplicate standalone explorers. F14/F33/F34 deliver production UI; early capability states are available before their completion, but full F24 closure requires all consumers.<br>7) UI shows only implemented capabilities/languages/DB sources and explains absence: not_configured, unsupported, unavailable, indexing, partial, stale, failed. PoC/experimental is not called production-ready; the product selects an engine on evidence, and internal backend settings are not imposed on the user. | F05, F10, F26, F27, F29, F14, F33, F34 |
| PAOS-FUNC-25 | P2 · Documentation | Align current product statuses and criteria | One current PRD/architecture/plan/registry pointer with history preserved. | The plan and documentation clearly show what works, what is limited, and what awaits verification. | 1) Current scope/status/acceptance do not conflict with historical implementation_not_started/API-only blocks: history is explicitly marked and routed.<br>2) F01–F34 and M5 have a single owner/status/source; implemented does not substitute for human/live acceptance.<br>3) Synchronize only changed claims and RU/EN registry; validators/docs tests pass, old 56 cards are preserved.<br>4) Current docs-site checks no longer report missing web/accessibility.html and web/pilot.html in RU/EN; search/sitemap/switcher parity is confirmed on an explicitly selected build. Site publication and promotion are separate.<br>5) Docs distinguish Sources, F26 file tree, F27 scanning, F28 inventory policy and F29 discovery; API/coverage versions, recovery and limitations are documented in existing PRD/architecture without claiming automatic repair or full semantics.<br>6) F30–F34 contain upstream URLs, research date, selected version/commit/license and actual PoC receipts when executed; README claims are not presented as local measurements. PRD/architecture/UI help describe Map/Database/usages tabs, read-only sources, export, coverage and fallback; links and RU/EN are aligned. | — |
| PAOS-FUNC-26 | P2 · Extension | Add a project file browser | Graph-independent directory and safe-reader API with lazy loading, stable links and bounded responses. | The user sees the selected folder structure and opens accessible files even when the index is not ready or the language is unsupported. | 1) After registration the Files section is available without a graph or completed scan; nested and empty directories, source files, configurations and binary files as metadata are visible within allowed F28 policy.<br>2) Expanding a directory loads only the needed branch; pagination and filters show selection bounds; filename/path search explicitly states scope. Metadata includes relativePath, type, size, modifiedAt and access state.<br>3) Text is read by a separate request with root identity, revision, size and encoding checks; binary/oversized/unreadable receive explanations. Extensions unsupported by the indexer do not hide files. HTML/scripts are not executed during preview.<br>4) No root escape through traversal, symlink/junction/hardlink or directory substitution; sensitive content is not exposed. Selecting a file does not send the whole project to a model or grant execution authority.<br>5) The selected path can be copied and used as a file reference; Control-plane is a filter over actual paths. Project switches and late responses do not mix trees; RU/EN, keyboard, focus, empty/error/loading are tested.<br>6) File/line navigation supports future transitions from Map/Database/code usages and return to the selected file; inaccessible/deleted source is explained. F26 does not wait for F30–F34; an absent capability's backend action does not display a false result. | F28 |
| PAOS-FUNC-27 | P2 · Extension | Make scanning a managed background job | Persisted scan IDs and stages, bounded worker, idempotency, cancel, retry and recovery separate from project registration. | The project is available immediately after registration; the user sees progress, partial results and how to continue after failure. | 1) Registration is saved once and returns an accessible project without waiting for full traversal; scan status includes scanId, root identity, policy version, inventory/documents/code/analysis stage, start/update times, counters and partial/error reasons.<br>2) Repeated Add/retry including after restart does not create another project or duplicate work; concurrent requests for one revision merge or receive an explainable conflict. A changed root does not continue the old job.<br>3) Cancel stops further work and late publication; retry starts with an explicitly defined revision. Restart recovers or moves the job to recovery_required/interrupted; unfinished work does not become completed.<br>4) Define time/memory/entry and concurrency budgets; failure of one analyzer preserves allowed results of other stages. Readiness of one index does not mean complete project analysis; an unconnected analysis adapter displays unavailable.<br>5) State and last successful coverage remain available after opening Settings/project and restart; events or bounded polling do not overwrite a newer revision. Scan bookkeeping stays in the PAOS profile; target workspace is not changed.<br>6) A versioned analyzer contract permits code/schema/code_database stages with separate capabilities/status/progress, cancellation and atomic publication. F30–F32 evaluate external executors in isolation; F14/F33/F34 connect only selected ones; F27 does not depend on their implementation or automatically run installers. | F28 |
| PAOS-FUNC-28 | P2 · Architecture | Unify inventory, coverage and exclusions | Shared path, revision and coverage contract for directory/document/code consumers with separate listing, reading and indexing rights. | Files do not disappear from the overview because a language analyzer is missing; users understand what was found, skipped or inaccessible. | 1) The contract distinguishes discovered, readable, indexed, unsupported, excluded and error; counters define different stages and do not sum overlapping sets as total files. Empty and unknown differ; no suitable code does not imply complete analysis.<br>2) The file tree is independent of indexer extensions. .gitignore and project include/exclude have explicit precedence and separate visibility/indexing rules; ignore grants no access. Sensitive paths/content remain protected even with include override.<br>3) Report applied policy version, skip reasons, limits and partial coverage. Heavy generated/vendor directories are not read unnecessarily; allowed metadata disclosure does not remove content-reading restrictions.<br>4) Individual file error, size overrun or unsupported encoding preserves other permitted entries; directory-level denial marks incompleteness. Root identity drift, root escape attempt or unreliable revision blocks publication of unsafe results.<br>5) Bounded/paged inventory supports normalized relative paths, Unicode/spaces and Windows case semantics; links and race conditions do not expand root. Identical policy/root/revision yield consistent references and reasons across consumers.<br>6) Policy changes invalidate affected snapshots; file metadata does not require reading all sources. Positive/negative scenarios and load boundaries are tested; project sources remain unchanged.<br>7) PoCs and future adapters apply the same root/policy/read/index rules and show coverage mismatches; third-party indexers do not bypass exclusions or create caches in the target. Discovered DB/ORM/migration candidates are metadata, not permission to connect or run migrations; scan limits and sensitive paths remain protected. | — |
| PAOS-FUNC-29 | P2 · Extension | Connect core discovery to project onboarding | Versioned read-only adapter to existing discovery/first-run analysis with provenance, limitations and invalidation. | After adding a project, stack, structure, Control-plane gaps and grounded next steps are visible, not only graph node count. | 1) Before build choose reuse of existing core discovery/first-run modules and deployment/runtime contract. Unavailable Python/adapter/version gives explicit unavailable; dependency installation and an alternative full scanner are not started automatically.<br>2) Analysis runs as a separate F27 stage, uses agreed F28 inventory policy and returns schema version, source revision, stack/components, control-plane coverage and findings with sources/confidence/limitations.<br>3) Discovered scripts/configs are analyzed only as data: project commands, tests, hooks, models or providers are not executed; target files are not created or repaired. Control-plane proposals remain proposals.<br>4) Empty project, no Control-plane, Python-only, mixed stack and unsupported language get explainable results without invented completeness; timeout/error preserve the available tree and coverage already obtained.<br>5) File, root or inventory policy changes make prior findings stale; retry and restart do not mix revisions. Findings are accessible from the selected project in RU/EN, linked to permitted file references and reveal no secrets.<br>6) Discovery shows language/ORM/DB/schema file candidates with source and confidence for F14/F33/F34, without opening connections or running migrations. Project overview offers Files/Map/Database routes by capability; missing adapter is not substituted by third-party auto-install. | F27, F28 |
| PAOS-FUNC-30 | P2 · PoC | Evaluate dependency-cruiser for JS/TS dependency graph | Evaluate reuse of an import analyzer instead of extending the current lexical parser; agree JSON adapter and edge semantics. | User and agent see verifiable file dependencies, cycles and a path to the change location. | 1) Before running pin version/commit, MIT and distribution licenses, Windows/Node compatibility, fixture corpus, current lexical graph baseline and time/RSS/response-size budgets; results are not inferred from README.<br>2) Synthetic JS/TS fixtures cover ESM/CommonJS, tsconfig aliases, re-exports, cycles, missing imports, dynamic import and monorepo boundaries; import is not called a function call. Compare known expected edges to output: list false positives/negatives and unresolved.<br>3) JSON adapter preserves normalized path/root identity, source revision, edge type/direction and evidence; respects the agreed F28 contract without depending on completion of its implementation. Configuration is passed by PAOS as data: target JS-config/scripts/hooks are not executed; target hashes do not change.<br>4) An isolated prototype of the existing Map has Dependencies mode: file search, incoming/outgoing, type filter, path/cycle highlighting, file/line navigation and synchronized graph/list/Mermaid. Errors and unsupported are shown; scenario peer review is not human acceptance.<br>5) Compare time, files/context volume and result correctness with baseline on identical change-location tasks; parser failure/timeout does not hide the tree. Deterministic benchmark requires no provider calls; model evaluation only with separate exact authorization.<br>6) Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.<br>7) The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance. | — |
| PAOS-FUNC-31 | P2 · PoC | Evaluate codebase-memory-mcp as an agent indexing engine | Evaluate SQLite-backed index, multilingual relations, queries and management of a separate native process via a versioned adapter. | Agent receives small relevant context and an explainable change path, while user sees the basis of search. | 1) Pin version/commit/license and distribution dependencies, Windows packaging, supported languages/relation types, workload and budgets. Comparison to current search uses the same ground-truth fixtures and tasks as F30; F30 need not finish first.<br>2) Test search/definition/references/call path/impact and related tests only for claimed capabilities; publish measured precision/recall, unresolved and unsupported. Bounded responses provide file/line evidence, revision, truncation/pagination; stale index is not presented as current.<br>3) Measure cold/incremental indexing, rename/delete/branch-like change, cancel/retry/restart, two projects, memory/disk and latency; SQLite/cache/locks belong to the engine and are not opened by PAOS as an unofficial writable API.<br>4) On a disposable profile demonstrate daemon lifecycle/cleanup, timeout and child-process ownership; investigate account-wide coordination and another build/cache conflict. Do not terminate a user's daemon or change global MCP/skills/hooks/PATH, download models or send code externally. If isolation is incompatible with PAOS, result is bounded_adopt/reject, not a guard bypass.<br>5) Map prototype includes symbol search, callers/callees/path/impact, explanation panel and source navigation; unavailable engine, partial coverage, stale and exceeded budget states are visible. UI contract does not depend on engine internal tables; evaluate reuse of existing PAOS graph UI.<br>6) Comparative report defines F30/F31 roles: one selected backend or explicit language composition without duplicate/conflicting revisions. Before integration the engine respects F28 inventory policy; reject an option unable to restrict sensitive-file indexing.<br>7) Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.<br>8) The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance. | — |
| PAOS-FUNC-32 | P2 · PoC | Evaluate tbls for DB schema extraction and Mermaid ERD | Evaluate an external JSON/Mermaid schema adapter against built-in SQLite introspection and pin the schema snapshot contract. | Obtain a reliable table map without manual drawing or reading user rows. | 1) Pin version/commit/MIT/dependency licenses, Windows distribution, minimum SQLite-first scope and budgets; compare tbls JSON/Mermaid against metadata introspection of the existing SQLite driver. PostgreSQL and other DBMS are separate capability targets, not automatic scope.<br>2) Synthetic SQLite covers PK/FK, composite FK, UNIQUE/index, views, nullable/generated columns, self-reference and missing FK. Compare object and edge lists with ground truth; format/driver limitations and inferred relations are not hidden.<br>3) Use an explicitly selected read-only fixture/consistent snapshot; row data, credentials and DSN do not enter logs/output. Test locked/WAL/change-during-read, inaccessible and corrupt files; connection does not create a missing DB, migrate it or execute project config/extensions/hooks.<br>4) Result contains source kind, schema fingerprint/revision, tables/columns/keys/indexes/views, coverage and warnings; canonical JSON and Mermaid agree. Test name escaping and ERD size limits, no HTML/script execution.<br>5) Isolated prototype of the future Database section shows source, ERD and object table, table/column selection, search/filter and explicit no-database/unsupported/stale/error. Mermaid export requires no external service; tiny Mermaid is checked for required ERD semantics.<br>6) Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.<br>7) The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance. | — |
| PAOS-FUNC-33 | P2 · Extension | Add a DB map and project Database section | Versioned schema snapshots, schema diff and a provenance/freshness-aware read-only adapter for the chosen source. | Users browse tables and relations, understand source and freshness of the schema, and navigate to its definition. | 1) Before build select adapter, supported sources and budgets using F32; missing backend selection remains a blocker. Distinguish PAOS's own DB from the analyzed project DB. Discovering a candidate in the tree does not open it automatically: user selects a permitted source; external/live/credentials require exact authorization.<br>2) Contract distinguishes actual DB schema, static ORM/migrations and proposed relations. An unapplied migration is not presented as the current DB; executing migrations/project code/extensions is forbidden. SQLite-first read-only schema extraction reads no rows and does not create/change the DB; PostgreSQL scope is not inferred from tbls support.<br>3) Add Database to project navigation with Schema and Changes tabs; Schema offers ERD/table mode, search, filters, table/column details, PK/FK/index/views and navigation to allowed schema/migration source. Settings retains registration and source selection, not a second independent browser.<br>4) ERD and table show one revision; composite FK and direction are correct, inferred relations differ from declared. Node selection syncs details/list, large schemas provide bounded subgraph and warning, Mermaid export escapes names, reveals no secrets and reports filters/coverage.<br>5) Changes compares two compatible snapshots: added/removed/changed objects; rename without proof is shown as add/remove or hypothesis. Missing baseline is explicit empty; source/policy drift marks stale, schema fingerprint and observation time are visible.<br>6) F27 database_schema stage has independent progress/cancel/retry/recovery/partial/error; failure preserves the previous successful snapshot marked stale and does not block Files/code. Unselected/missing DB is not_configured/none_found, not endless loading. Reject late responses from another project/revision.<br>7) Pass F32 API/adapter and browser scenarios on disposable fixtures: RU/EN, both themes, keyboard/focus, table alternative, deep link/back, restart and project switching. Target and control files remain unchanged before/after; no sensitive DSN/rows in UI/export/logs; runtime evidence is build-bound.<br>8) On F20 workload measure schema extraction, cold/warm view, large ERD, memory and response size; budget deviations have bounded outcomes. Update F24/F25 docs/capabilities for actually implemented scope; UI mock does not close acceptance.<br>9) The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance. | F26, F27, F28, F32 |
| PAOS-FUNC-34 | P2 · Extension | Link code to tables and show change impact | Add provenance-aware code→query/ORM→table edges resolved in compatible code/schema revisions and bounded impact queries. | User and agent see which code reads or changes a table and what to check when its schema changes. | 1) Before build choose a bounded language/SQL/ORM matrix based on F30/F31/F32; include code call paths only with confirmed semantics, import edges do not substitute for CALLS. Fix ground-truth cases and precision/recall thresholds before measurement.<br>2) Relation stores file/symbol/line span, query or model evidence, table identity/source, operation read/write/schema/unknown, extraction method/confidence and code+schema revisions. Dynamic SQL, naming heuristics, aliases and untraceable calls remain inferred/unresolved; unknown is not treated as absence of dependency.<br>3) Test raw SQL, chosen ORM, joins/aliases, identical table names in different sources, rename/drop, generated/dynamic query and unsupported language. Code/queries are not executed; secrets/DB rows are not extracted; precision/recall and limitations are presented per supported type.<br>4) Add Code usage tab to Database: table → read/write locations → file/line; existing Map gets DB-link filter and path/impact panel. File reader supports navigation to linked tables. Selection/deep link/back/filter stay within project; arbitrary relations are not drawn as confirmed.<br>5) User switches confirmed/inferred and read/write/unknown, opens edge evidence and sees incomplete impact. Accessible table/list duplicates graph meaning; RU/EN, both themes, keyboard/focus, empty/unsupported/partial/error/stale and large results are tested in browser.<br>6) Agent queries return bounded source-backed paths and test candidates, truncation/cursors and both revisions; source rename/delete/change invalidates only the compatible snapshot. Mixing code/schema from different projects or stale revisions is forbidden; rebuild/restart/cancel/retry are tested.<br>7) Compare locating changes on agreed tasks without and with relations: correctness, missed affected files/tests, context and time; no promises of complete runtime call graph. F20 budgets and F27/F28 guardrails are met; one analyzer failure does not block tree and schema map.<br>8) Documentation explains schema ERD versus code-to-table impact; release claims and capability states align with F24/F25. Closure requires working UI/API/agent-contract integration, not only a schema or prototype.<br>9) The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance. | F14, F33 |

## Existing M5: references without duplicated state

Status at owner read time: `planned`. Always read current status in the original M1–M5 group.

| ID | Task | Technical value | Product value | Original card acceptance criteria | Dependencies |
| --- | --- | --- | --- | --- | --- |
| PAOS-0047 | Optional Sign in with ChatGPT | After admission implement a separate SIWC route, consent, PKCE/scopes, refresh/restart/resume and preview capability matrix | Eligible user can use an authorized ChatGPT plan without a second working application. | Only after confirmed exact paid/local route admission: identity and plan scope checked, refresh/resume does not duplicate work, unsupported tools hidden with reason; API route does not depend on this task. | PAOS-0039, PAOS-0044, PAOS-0046 |
| PAOS-0052 | Team PostgreSQL and pgvector profile | After a separate M5 team design/start decision implement server repository, dialect migrations, tenancy/RLS, lexical and versioned vector index; hosting/auth/runtime design gate before code | Team works with shared current state and search within its permissions. | ST-10: domain parity, negative tenant/pool tests, filtered search; embedding model/privacy approved; lexical fallback; hosting/auth/runtime placement agreed; local M4 does not depend on M5 | PAOS-0048, PAOS-0049, PAOS-0051, PAOS-0030 |
| PAOS-0053 | Transfer local project to team workspace | Versioned logical export/import, actor/tenant mapping, blob checks, final delta and one-authority handover | User transfers a project to the team with prior tasks and history, without conflicting writable copies. | ST-11/ST-AC-08: UUID/key collisions, identity mapping, counts/hashes/FK, final delta, rollback; credentials/pending approvals/commands excluded; local read-only after switch; no bidirectional sync | PAOS-0056, PAOS-0052 |

## Shared execution and acceptance contract

- First reproduce a defect on the current revision; RED from broken setup is not accepted. A limitation is a defect only against the accepted contract.
- Checks must identify sources/dependencies, environment, synthetic dataset, observed outcome and evidence boundaries. Mock UI, connected App and full execution are different states.
- No tokens, secrets, raw private chat or real customer data in reports. Pairing material stays in memory; provider calls and real profiles outside synthetic checks require exact authorization.
- Design-approved, implemented, technically verified and human accepted are different facts. Extension tasks F11–F17 cannot be completed by design alone; implemented requires all behavioral AC and checks.
- Technical and product fields are mandatory on each new card; completion receives an actual date only after execution. All future commands below are a plan, not a log of executed checks.
- Rollback for each task preserves user files and other work. Planning creates no branch/commit/PR and changes no application, hook/trust or permissions.

## Readiness to start tasks

Package status: `proposal_staged`; this is the complete backlog, not a `plan_ready` claim for all implementation. Structural validation of the plan does not close the following gates.

| Gate / tasks | Status | Owner and required evidence | Risk before closure |
| --- | --- | --- | --- |
| Reproduce F01–F07 | present_unverified | tester: RED and specific source revision; AC and Source in cards | static inference may differ from runtime |
| Architecture F08/F09 | proposal_staged | architect: boundary/contract review in existing architecture and F20 measurements; existing-capability scan before new code | unnecessary refactoring, changed public behavior |
| Telemetry F11 | applicable_missing | architect/product-manager: tracking sources, ownership, privacy/retention, unknown policy | invented metrics and double counting |
| Extensions F12–F17 | approval_required | owner + architect: each card's design gate, supported capabilities, build estimate | unavailable API, breach of write/enforcement/distribution boundaries |
| F19–F22 scenarios | proposal_staged | tester: protocol → checks → receipts in Completion Report; exit0 and all scoped AC expected without substituting native execution | synthetic and live evidence may be confused |
| Human pilot F23 | applicable_missing | product-manager + owner: agreed protocol, participants/consent, baseline, observable results over 14 days | product value remains a hypothesis |
| Docs tooling for current planning | not_applicable | existing Python docs checks and Markdown suffice; site, CI and new dependencies are unchanged | rendered-site freshness is not claimed |
| Coding standard for current planning | not_applicable | code is unchanged; use current coding-standards workflow when implementation starts | plan does not replace source review for a specific slice |
| GitHub PoCs F30–F32 | proposal_staged | architect/tester: pinned version/license, synthetic ground truth, budgets, UI prototype, adopt/bounded_adopt/reject; current planning does not authorize execution | upstream promises and isolation/packaging incompatibility |
| DB map / code links F33–F34 | applicable_missing | architect/UI owner: PoC decisions, source/read-only contract, wireframes and scoped API/browser evidence before closure | schema does not equal runtime usage; prototype does not equal production UI |
| M5 | approval_required | original cards own admission/team design and migration gates | team/provider work cannot start from a reference in this matrix |

Business/product hypothesis: correct state preservation and understandable scope should reduce work errors; confirmation is F23, not a fact established by test count. Outcome scope is the local App-active product; repeat-use observation is 14 days; delivery metrics and user value are separate. Extensions with new domain/API/storage boundaries require current existing architecture/ADR and agreement on invariants before build; no compulsory new methodology, portal or template set is created now.

## Addendum: files and scanning — 15.11.2026

The owner authorized only a plan update. F26–F29 were added; AC of ten existing F02/F09/F10/F14/F18/F19/F20/F23/F24/F25 tasks and hard dependencies of seven were clarified. All 29 group tasks remain planned; three M5 entries reference the prior state owner.

Selected boundary: project registration → available file tree and read-on-demand → managed scanning → separate inventory/documents/code/analysis results. “File is visible”, “file can be read”, “file is indexed” and “command may execute” are distinct facts. An unsupported language does not hide a directory. Model context is prepared separately, without automatically sending the whole project.

Source-backed basis: [Sources](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts) lists six Control-plane files; [registration](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts) saves the project, then waits for source/code scan; [inventory](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/sources.mts) uses fixed exclusions and limits; [core discovery](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py) and [first-run](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) exist separately from the checked Web onboarding. This is a static conclusion, not a new runtime receipt.

| Design gate | Status / owner | Required before build |
| --- | --- | --- |
| F28 inventory policy | proposal_staged; architect + security reviewer | Shared root/path/revision/coverage semantics; listing/read/index separation; ignore precedence; budgets; fail-closed boundary |
| F26 directory API/UI | proposal_staged; builder + product-manager | Read-only tree and preview, pagination, empty/error/keyboard/RU/EN; file does not depend on indexer language |
| F27 scan lifecycle | proposal_staged; architect + tester | Durable state machine, recovery/idempotency/cancel, profile storage and migration/rollback contract; bounded workload |
| F29 core adapter | proposal_staged; architect + plugin-runtime-builder | Reuse rather than independent scanner; versioned structured result, runtime availability, read-only invocation and stale policy |
| F19/F20/F23 coverage | proposal_staged; tester/product-manager | Expanded fixtures, measurable budgets before benchmark and separate human acceptance |

Shared ownership: F28 owns inventory contract; F26 directory API/reader; F27 orchestration/profile state; F29 core adapter/result. Serialize changes to shared application.mts, client.ts, storage and onboarding. F18/F24 integrate completed contracts, F19/F20 verify them together. New work-location names are plans; implementation files are not being created now.

Mandatory test matrix: empty/no-Control-plane, Python-only/mixed stack, large monorepo, Unicode/spaces, wide/deep directories, ignored/generated/vendor, binary/large/invalid-encoding/unreadable, symlink/junction/hardlink/traversal, root replacement, file rename/delete during scan, two projects, cancel/restart/retry. For F20 first fix budgets and hardware/cache; do not remove limits to pass tests. Reuse existing guarded source helpers after contract verification.

## FUNC-G01 — execution results {#func-g01-results}

Status: **closed / implemented_locally_verified**, 7/7 tasks F01/F03/F04/F05/F06/F07/F08. Group machine status is derived from its seven members; root JSON remains in_progress because 27 tasks in other groups remain planned. Original AC, IDs, priorities, estimates, Depends on/Blocks/execution_order, delivery-group definitions and M5 references are preserved. The owner authorized implementation on 2026-11-15; no Git/publication/provider/real-credential operations.

| Check | Observed result / receipt |
| --- | --- |
| F01 initial RED | Manifest mismatch with the current lockfile; `.tmp/func-g01-runtime/manifest-red.log`, `native-red.log`. A pin overwrite was never treated as qualification. |
| F01/F08 final native | Candidate and production default passed Discussion/Planning/Execution, inside write/outside+private-temp EPERM, binary/lock/adapter drift before spawn, repeat broker start/Stop and cleanup. `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, `native-default-final-escalated.log`; focused runtime12/12. |
| Native tuple | Codex0.167.0, Node26.5.0, Windows10.0.26200 x64, SQLite3.53.3. Adapter `fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5`; lock `f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac`. Candidate receipt SHA `a2cad642d6f3bc416a04a954f4bbbfa009aae75d5aeacc77bac3f940313dcf4a`. |
| F03/F04 browser | `node tests/web/single-window/func-g01-drafts-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>`:54/54, `.tmp/func-g01-drafts/evidence-C6lIVM/result.json`. Production UI/HTTP/SQLite, concurrent writers and exact ACK revision; source hashes and fixture cleanup. |
| F05/F06/F07 browser | `node tests/web/single-window/func-g01-dashboard-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>`:30/30, `.tmp/func-g01-dashboard/evidence-MIaKso/result.json`. RU/EN partial/loading/retry/all-failed/complete, queue parity/reorder/null, updatedAt/create/edit refresh, desktop/mobile readability and screenshots. |
| Shared contracts | The AST guard first detected two reverse import edges; after relocation, direct/compatibility identity, M1/M2 decoder and theme/locale checks pass. `node --test tests/web/contracts-boundaries.test.mts tests/web/task-profile.test.mts tests/web/m2-profile.test.mts tests/web/theme-locale.test.mts`; all15 are also represented in the full Web receipt. |
| Typecheck/build | `npm run check:web-m1` and `npm run build:web` exit0. Build repeated after the CSS visual repair. The >500kB bundle warning is retained; F09/F20 optimization was outside this group. |
| Full Web + environment repair | `npm run test:web-m1`:507 tests,492 pass/11 fail/4 skip because sandbox EPERM prevented link/symlink fixture creation; original `.tmp/func-g01/web-final.log` retained. Exactly15 affected cases rerun on the authorized executor:15 pass/0 fail/0 skip, `.tmp/func-g01/web-boundary-retest.log`. Overall507 unique tests passed in two contexts; the original full run is not called green. |
| Review | Independent implementation review `/root/func_g01_review`: closed_allowed; architecture review preceded F08. Cycle2 CSS/readability delta: closed_allowed. The reviewer confirmed current source/asset hashes and corrected the historical EN machine-state link. |
| Final source/state gates | `tools/check_docs.py --paths`20 changed Markdown sources passed; docs unittest3/3; `validate_task_matrix.py` RU/EN exit0; `validate_task_state_consistency.py .` exit0; `git diff --check` exit0. Checked34 RU/EN/JSON statuses, unchanged27 task objects/cards, all original AC/dependencies/estimates/order/groups/M5 references and browser source hashes. Group evidence moved before the cards after a validator rejection attributed angle-bracket command arguments to the final F34; original F34 unchanged. |

Rerun reasons and rejected attempts are retained: Chromium startup without required executor permissions (0 checks), native MXC unavailable, initial F03/F04 and ACK/refresh race RED, premature browser assertions before async save completion, mobile readability RED. Test waits use observed clean/enabled state; product guards, sandbox policy and Chromium sandbox were not weakened. The first build revealed toSorted absent from the frontend TypeScript lib; a copied array with standard sort is used. The AST regression reuses the installed public parser because the TypeScript7 package does not expose the previous JS AST API.

Code contract: existing_capability — existing handlers, memory Maps, StoreReceipt, strict decoder/preferences and installed parser; smallest_safe_patch — reset/CAS/projection corrections and two compatibility seams; invariants — original CAS, project isolation, unknown≠0, exact runtime pins; dependency_decision — no_new_dependency; risk_selected_tests — browser/state/decoder/import/native plus demonstrated link-fixture retest; comment_decision — concurrency/order/boundary intent documented; performance_applicability — no benchmark or budget change; evidence_and_gaps — current source hashes/tuple with separate receipts.

Documentation impact: updated — frontend state-management/components, backend lifecycle/modules, architecture containers, testing map, RU/EN registry, these cards and owning JSON; REQUIREMENTS/PLAN/TEST/RUNLOG synchronized. EVALS/prod_test no_change_needed: eval policy and historical Batch39 unchanged. API docs no_change_needed: endpoints/payload/schema/errors preserved. Atlas review no_change_needed: existing diagram container/runtime boundaries unchanged; ownership/import detail recorded in architecture/modules. No site build/publication or dependency installation. No human-acceptance, provider/model behavior or broad production-readiness claim.

## FUNC-G02 — protocol and engine results {#func-g02-results}

Current status: **implemented / poc_research_locally_verified; 3/3 closed**. The2026-11-15owner request authorized full F30/F31/F32 execution; original planning_only phrases in the AC describe the earlier planning authority, not this request. Other FUNC/M5 work is not started. Protocol/ground truth pinned before measurements in `tests/fixtures/func_g02/protocol.json` and `corpus.json`; protocol SHA `4d8c4760f20f65c3dde015067ff6e5e59eb6835bca2f89afc99138b43f0639be`, corpus SHA `d727efe0e2fe11a9303262addadbbfb73ab97ec5af844ed585acdbbfe537f11a`.

| Task | Engine decision and supported boundary |
| --- | --- |
| F30 | bounded_adopt: dependency-cruiser18.6.0 + isolated TypeScript5.9.2 for imports only.10/10expectededges, precision1/recall1; lexical baseline7/10. Change tasks3/3vs2/3. Cold median817.39ms vs218.27ms;200additionalfiles961.49ms/146.33MiB.4model tests and17engine scenarios. |
| F31 | reject for the current Windows workspace profile: codebase-memory-mcp0.12.1 refuses admission beforeindex.12integrity/admission/preservation checks and3unit tests; version/help passed. Index/query/lifecycle/RSS after rejection are unexecuted with null metrics. ACL/source cause is inference, not an internal trace. |
| F32 | reject tbls1.96.1 as authoritative SQLite metadata: generated omission, valid identifier failure and missingDBcreated with testedread-onlyDSN.26observations=23positive+3candidatefailures. Explicit node:sqlite metadata alternative; tbls200table367.996ms; current corrected Node baseline5.945ms, separately measured in-process. Earlier16.892ms baseline retained with its old provenance. Effective-nullability regression6/6 passed; native receipts unchanged. |

Before measurements: pinned version/commit/license, shared synthetic JS/TS/Python corpus, independent expected import/call/change-task oracle, SQLite DDL ground truth,30s small/60s large index timeout,1MiB stdout,1024MiB RSS/cache,200-file/table workload,3cold runs. Query budget5s; prototype interaction budget1500ms. F28/F20 contracts are draft-only; production implementation is not a prerequisite. External tools receive an allowlisted read-only projection; config/secret exclusions do not become graph data. Target JS-config/scripts/hooks are not executed; no model/provider/network during measurement.

Versioned proposal `paos_engine_poc_snapshot_v1`: meta engine/version/sourceRevision/rootIdentity/policyVersion/coverage/capabilities/warnings, stable node IDs/path/line and typed directed edges/evidence. Import≠call, unknown≠false/zero, unresolved/inferred never promoted to observed. Engine SQLite/cache is not writable PAOS state. F14 gets an import-only F30 proposal + existing bounded lexical baseline; multilingual semantic/call path remains a gap. F33 gets an explicitly selected Node read-only metadata adapter proposal, not silent tbls fallback. Production F14/F33/F34 integration remains planned.

Pre-build UI design: existing V3 read-only explorer — compact project/mode/source/coverage bar, outline → graph/list/Mermaid → evidence inspector; mobile list-first with collapsible details. URL-only state, project changes clear incompatible selection, source-line→Back. Import graph and declared-FK schema have distinct semantics; visible direction, keyboard/table alternative, zoom/reset, RU/EN, light/dark, loading/empty/partial/error/unavailable/stale. Unavailable F31 never shows a fabricated measured graph; proposed symbol/call fixtures are separate. Protocol/wireframe peer review `/root/func_g02_cbm`: approve; renderer compatibility tested locally.

Evidence: `.tmp/func-g02/f30/result.json`, `tool-audit.json`, `snapshot.json`; F31 `result.json`, native preflight/ACL/source/checksum receipts; F32 `result.json`, `dsn-mode-probes.json`, raw JSON/Mermaid and selected snapshot. Three F32 candidate failures and F31 admission rejection are retained, not called green. Later metadata/UI repair does not rewrite native findings or benchmark provenance. Final prototype/typecheck/build passed; browser22/22 and combined model/preview tests22/22. Build-bound evidence: `.tmp/func-g02/prototype-build.json`, `prototype-browser/result.json`. Installed tiny Mermaid rendered canonical erDiagram; prototype README owns preview commands.


Independent review `/root/func_g02_review`, separate_reused_context, two cycles: SQLite effective-nullability P2 fixed and accepted; final two UI P2 repaired (project-bound direct URLs/export and filtered ER parity). Root inspected the delta, new model/browser regressions, current source/build/harness hashes and desktop/mobile screenshots: closed_allowed. The independent verdict before those final repairs was partial_only; no third review cycle is claimed. F31 downstream capabilities remain unexecuted after admission rejection; F32 three candidate failures remain negative evidence. These close research decisions, not product features.

Closure commands: combined22-unit command recorded in machine state, `node tests/web/poc/func-g02/prototype-build.mts`, `node tests/web/poc/func-g02/prototype-browser.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH`, matrix validators for both languages, scoped source-docs and preservation checks. Preview: `node tests/web/poc/func-g02/prototype-preview.mts`. Control-plane sync updates REQUIREMENTS/PLAN/TEST/RUNLOG; EVALS/prod_test no_change_needed, no changed AI behavior or production-test evidence. Human acceptance and production integration remain outside PoC closure.

Final static closure: both task-matrix validators passed; source-docs19 passed;31 unrelated task objects and31 cards per language, all original AC/priorities/estimates/dependencies/groups and M5 preserved; current production sources unchanged. Preservation and source/build/harness binding receipt: `.tmp/func-g02/closure-consistency.json`; diff check passed. The historical pre-relocation M5 hash was not the current baseline: corrected verification compared the unchanged task-start Git source. No M5 file was changed.

## FUNC-G03 — execution and decisions {#func-g03-results}

Status: implemented / locally_verified,7/7; group exit passed. Owner authorized F28/F26/F27/F02/F29/F10/F18 implementation; original planning_only phrases refer to prior planning. Root owns shared HTTP/API/storage and task/docs integration; a separate owner implements the lower inventory. Other27 task records, closed G01/G02 and M5 are preserved.

F28: independent read-only inventory below project-sources; separate listing/read/index permissions and stage counts, explicit partial coverage, parser-independent metadata tree. Hard root/link/sensitive denial precedes exclude/include/gitignore. Root/policy/revision changes invalidate snapshots; lazy direct listing and bounded recursion.

F27: registration does not await scan. Versioned JSON+CAS in profile-owned store_meta reuses the immutable SQL schema, never task/document pseudo-entities. Cancellation fences analyzer publication; an outer timeout race alone is insufficient. Restart interrupts unfinished jobs and late results cannot publish.

F29: existing Python core receives only an allowlisted F28 projection in an owned temporary profile. It does not rescan the real root. Output is target root/policy/revision bound and explicitly partial; unavailable Python/version/timeout never triggers installation or another scanner.

Accepted test seams: inventory metadata/checked read/exclusions; authenticated directory/read/scan/analysis API; durable scan CAS/cancel/restart; artifact path normalization; execution file preflight; UI navigation/late-response/freshness/dirty-draft protection. Original AC and assigned tests map each task to scenarios and evidence owner; root owns combined API/browser/native activation evidence.

Code contract: existing_capability=checked-handle readers/codeIndex worker/core discovery/LocalStore store_meta/createLatestRequest/V3 UI; smallest_safe_patch=lower inventory and bounded directory/job/analysis adapters with sequential shared wiring; invariants=root/policy/revision isolation, no target mutation or secret disclosure, cancellation before publication, dirty drafts preserved; dependency_decision=no_new_dependency; risk_selected_tests=public seams/security/recovery/browser; comment_decision=policy/CAS/publication intent; performance_applicability=bounded metadata/workers/projection/polling; evidence_and_gaps=current synthetic checks passed, no provider/human/release claims.

### Final evidence and boundaries

All seven members F28/F26/F27/F02/F29/F10/F18 are implemented and checked against their original AC. Other27 task objects/cards, original priorities/estimates/dependencies/order/groups and3 M5 references remain unchanged. Global task total:17 implemented /17 planned. Group closure is derived from members and exit evidence; it does not start another group.

| Contract | Current evidence |
| --- | --- |
| F28 inventory / F26 Files | lower16 plus Files9, policy/CAS/consumer regressions; Add→immediate tree→plain reader→line/hash/copy/back; actual link/root/policy denial |
| F27 lifecycle | persisted queued/CAS/cancel/retry/restart; registration replay and late graph-publication rejection; real inventory/documents/code/analysis stages |
| F02 references | structured artifacts + legacy paths/backlinks/task filters, stale raw pins, excluded/deleted source denial; production UI backlink→task |
| F29 core | real isolated Python/core9 focused cases plus HTTP restart/stale proof; allowlisted projection, source/confidence/candidates, no target scripts/DB open |
| F10 preflight |32/33 paths,65536/65537 and524288/524289 raw bytes; operations/rename/pins; UI blocked Send retains draft; server and native policy fences |
| F18 freshness | atomic snapshot/stamp, second-channel stale, overlay refresh, dirty draft/original CAS409, disposed polling; modified/renamed source and stale analysis |

Final mandatory Web suite `npm run test:web-m1`: **594/594,0skip**, `.tmp/func-g03/full-web-native.log`. Native environment was selected for the full run because the sandbox had rejected exact synthetic link/junction setup. Earlier setup failures remain in their original receipts; they are not behavior RED. `npm run check:web-m1` and `npm run build:web` passed; the existing >500kB chunk warning remains (performance owners F09/F20). Production UI browser **19/19**, RU/EN × light/dark Files at1440/390px, source/build hashes and screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Clipboard, deferred response delivery and the UI no-Send runtime boundary are labelled fixtures; core/HTTP/SQLite/FS are actual local implementations. No external requests/page errors; target hashes preserved.

Native candidate and production-default inspector both passed on adapterRevision `64cd3b58c5688e0673cb3bea5ea250817e10eb281d07c9a4e293ade759f0d33e`; candidate receipt SHA256 `94643d3bee58f959281c18f9f099896959ab92a64ea6e4fc4d5c2ab05c52b450`. Receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`; production default uses no candidate exception. Discussion/planning deny writes, execution permits owned workspace writes while outside/temp writes are denied; drift rejects before child spawn, interrupt, broker recreation and isolated-home cleanup passed. `.py` bridge bytes now participate in executable source qualification (observed RED/GREEN). The initial sandbox rpc_rejected receipt is retained. No provider/model/auth credential operations were used.

Independent review `/root/func_g03_review`: cycle1 separate_fresh_context reproduced a P2 captured-policy race; root fixed the common cause in final registry fences and atomic task/registry observation. Deterministic RED2/2 and consumer RED3/3 are retained; cycle2 separate_reused_context independently verified5/5, tester_verdict=closed_allowed. Root repair regression30/30 and affected consumer/API20/20 passed; broader affected58 had57pass/1sandbox link setup failure, exact native retest1/1, followed by full native594/594. Failed setup/probe directories and the temporary executable are cleaned within owned containment; receipts remain. No source/diff protections were waived.

Documentation: changed canonical API/events/backend/recovery/data-flow/inventory/discovery/queries/security/transactions/frontend/navigation/state/components and RU/EN registry updated; source-docs30 and both matrix validators passed. Root REQUIREMENTS/PLAN/TEST/RUNLOG synchronized. EVALS/prod_test no_change_needed: no rubric, model/prompt or Batch39 evidence changed. Atlas/MkDocs no_change_needed: existing architecture data-flow owns this runtime boundary; no lifecycle route or navigation page was added. Final preservation/source/build/native bindings are recorded in `.tmp/func-g03/closure-consistency.json`.

Accepted limits: existing desktop distribution omits checkout core/catalog and explicitly returns unavailable; packaging belongs to F17. Projection/output/time are bounded, portable OS RSS hard cap and broad performance qualification belong to F09/F20. F14/F33/F34 own future Map/schema/code-table consumers. Synthetic local closure does not establish provider execution, human acceptance, mass-project or commercial release readiness. No dependencies were installed; real profiles/credentials/targets, global configuration and Git/publication were not changed. Rollback only this slice's hunks; after executable changes requalify the manifest, preserve user files and earlier G01/G02/M5 evidence.

## FUNC-G04 — execution and decisions {#func-g04-results}

Status: implemented / locally_verified_with_measured_limits. Owner authorized F20/F09/F14/F33/F34. G03 working source is the preserved dirty baseline193files, HEAD5a9c87b; other29task records and M5 remain owned by their existing reports. Root owns shared storage/HTTP/API/App and status/control-plane synchronization; independent owners use explicit file boundaries.

Sequence: F20 protocol/baseline before F09 source fixes; F14 after measured fixes; F33 after explicit source/adapter design; F34 after compatible code/schema consumers. At most root+two specialists, then independent review. No Git/publication/providers/live databases/global installation/configuration.

F33 design decision: Node26 SQLite readOnly schema-only extraction of an explicitly selected project-local offline SQLite file, distinct from PAOS profile DB. No automatic candidate opening, copied DB bytes, rows, project SQL/scripts/extensions or PostgreSQL inference from tbls. Hard-link/reparse/root/policy/private checks and dedicated admission precede access. Windows native read lease holds target and root-to-target ancestors against write/delete while SQLite owns its second handle; fixed trusted PowerShell/C# helper, no policy bypass or installation. Node validates root/identity/policy after readiness; extraction closes before lease release. Existing sidecars, WAL header, busy lease or unsupported host fail closed. This avoids claiming pre/post path checks alone prevent ABA. SQL metadata uses bounded trusted statements/authorizer, time/output/SQLite limits; JS heap limits are not native-memory guarantees. Source hashes/policy rechecked before publication; Windows lease conformance must pass before feature closure.

F14/F34 language/backend and UI gates will be recorded here before their build, preserving F30/F31/F32 measured adopt/reject decisions and V3 design. Test seams are existing public APIs, source/scan snapshots, source selection, graph/schema/links queries and rendered navigation; synthetic native/browser fixtures are authorized, provider/human acceptance stays separate.

Code-change contract: existing_capability=F28checkedinventory/F27CAS/NodeSQLite/rolldown+TypeScript/V3D3Mermaid/LocalStore; smallest_safe_patch=measured read/cache fixes plus bounded source adapters and consumers; invariants=project/root/policy/revision/late-publication isolation and preservation; dependency_decision=no_new_dependency, installed/native capabilities first; risk_selected_tests=protocol/groundtruth, auth/path/read-only/recovery/cancel, API/browser/native; comment_decision=authority/lease/cache/semantic limits; performance_applicability=required F20 before/after; evidence_and_gaps=current measurements pending, no readiness claim.

### Production navigation and wireframes — selected before build

Technical design uses existing V3 tokens/components, D3, escaped Mermaid and a useful table/list alternative. It is selected for implementation; it does not claim human acceptance. Files, Map and Database are independent project navigation entries; Settings owns registration/source selection only.

| Surface | Desktop wireframe | Mobile and states |
| --- | --- | --- |
| Map | Dependencies/Symbols → search/direction/edge filters + revision/coverage → object list / graph-list-Mermaid / evidence drawer; incoming/outgoing, bounded path/impact, source line and Files links | List first; collapsible evidence; keyboard node selection and focus return; explicit zoom/reset; loading/empty/partial/error/unavailable/stale |
| Database/Schema | Source/revision/coverage + scan/cancel/retry → bounded ERD/table from one page → selected table columns/PK/FK/index/views; safe export and source definition where observed | Table alternative, search/type filters, selected object retained per project; no auto-opening candidates |
| Database/Changes | Compatible baseline/current revisions → added/removed/changed objects; rename remains add/remove without evidence | Explicit no-baseline/incompatible/stale; source switch never compares different databases |
| Database/Code usages | Table→read/write/unknown and confirmed/inferred/unresolved→file/span/evidence; compatible code+schema revisions, truncation/cursor, bounded agent context | Accessible result list and source line; Files reader links back to related tables, Map has DB-relationship filter and incomplete impact |
| Settings/Project | Explicit relative source + observed metadata pin + settings CAS → Select/Clear, then separate scan action | not_configured/none_found/unavailable/forbidden explained; no DSN/credentials or target scripts |

F20 protocol is pinned in tests/fixtures/func_g04/protocol.json before measurements: unchanged WEB-NFR thresholds, three rounds and bounded soak, real hardware/cache separately from reference4-core machine, full10k tasks/100k messages/~200MiB/1k files and exact boundary cases. API-visible latency is separate from rendered UI visibility/cold GUI. Budget failures remain observations and become measured F09 inputs.

### F14/F34 — production composition selected before build

- F14 uses installed public rolldown/utils.parseSync1.2.18 (OXC AST) for JS/TS/JSX/TSX/MJS/CJS/MTS/CTS and in-file lexical define/read/write/reference/call. Cross-file edges are imports/reexports, literal dynamic imports and unshadowed literal require, never runtime calls. A pure allowlist resolver uses F28-admitted paths and safely read root tsconfig baseUrl/paths only. JSON comments/extends/references/package exports/unknown aliases remain explicit partial/unresolved; target code/config is not executed. G02 ground truth target is precision1/recall≥0.9 for10 imports. Other languages remain unsupported.
- G02 dependency-cruiser18.6.0 retains its bounded_adopt import-only PoC decision; its isolated .tmp installation and TypeScript5.9.2 are not shipped product dependencies. Installed TypeScript7.0.2 does not expose legacy createSourceFile/resolveModuleName APIs. CBM reject remains. A public rolldown/experimental ResolverFactory probe rejected valid Windows paths under restriction and discovered parent package.json outside the projection without restriction, so it is not selected. The explicit production alternative is the installed AST plus a conservative deterministic allowlist resolver, with no silent backend fallback.
- Restart/eviction explicitly invalidates the memory graph; cursors bind cache generation and filters. Files stays independent. Rollback only reverts G04 parser/resolver/UI hunks while retaining F28 guards and G03 scans.
- F34 supports JS/TS+SQL literal SELECT FROM/JOIN, INSERT INTO, UPDATE, DELETE FROM and CREATE/ALTER/DROP TABLE, plus one Prisma static subset (schema.prisma model/@@map and literal file: datasource, traced PrismaClient/delegate). Tokenizer/AST separates comments/strings/aliases. Confirmed links require selected source binding through literal node:sqlite new URL(...,import.meta.url) or literal Prisma datasource. Cwd/env/dynamic/untraced/table-name-only matches stay inferred/unresolved.
- Evidence binds file/span/symbol/query/model/table/source/operation/method/confidence/reason to both code and schema revisions. Equal table names across sources remain separate. No SQL/Prisma/project execution, row reads, DSNs or runtime call-graph claims. Promotion requires per-kind ground truth, scope/revision/cancel fences, context≤32KiB and measured correctness/missed files/tests/context/time against static manual-search tasks.

Text-integrity note: the pre-build decision text was restored from its original temporary design packet after correcting inter-character Markdown escaping; original cards and AC are unchanged.

### FUNC-G04 — final evidence

All five cards (F20/F09/F14/F33/F34) are implemented; overall matrix: 22 implemented / 12 planned. Original acceptance criteria, estimates, dependencies, groups and M5 references are preserved. Closure is bounded local synthetic verification with measured limits; it does not claim all NFRs pass. Review: separate_reused_context, /root/func_g04_review, tester_verdict=closed_allowed.

Web: 658/658, 0 fail/skip (.tmp/func-g04/web-closure-native-final.log); typecheck and current-UI build passed. Browser: 18/18 with 204 source hashes, dist binding, 30 screenshots, four pages covering 200 objects, real API/native lease and service/profile restart; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json. Native candidate and production-default passed for adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b, with zero provider/model/credential operations. The current three F20 receipts are .tmp/func-g04/scale-closure/result-diagnostic-1794778219987.json; .tmp/func-g04/scale-closure/result-reference-1794778236139.json; .tmp/func-g04/scale-closure/result-filesystem-1794778628384.json. Their 133 inputs match current source; protocol 37c20aadc0d3474ef78cf86928e9ee1727be7bf415152fc393e92c8b079af625 is unchanged.

| Metric | Current closure run | Comparison |
| --- | --- | --- |
| Indexed search p95 / 36 | 159.06 ms | 500 ms |
| Command ACK p95 / 36 | 403.71 ms | 500 ms |
| Task page 50 p95 / 36 | 3.33 ms | 1000 ms |
| Commit → freshness API p95 | 404.80 ms | 1000 ms |
| Task Manager p95 / 3 | 504.80 ms | 1000 ms |
| HTTP creation after full seed | 1063.57 ms | 10 000 ms |
| Graph rebuild / 1000 files | 11475.70 ms | 60 000 ms |
| Graph status / 3 | 313.49 / 294.86 / 277.69 ms | 1000 ms |
| Soak | 120.15 s / 119 iterations | 120 s |
| Browser per-process backend/harness | 253.07 MiB | 1024 MiB |
| Browser aggregate sampled current | 1101.32 MiB | diagnostic only |

Cold history/catalog generations retain recorded 1000 ms deviations. Full 10k/10001-directory traversal ends in an explicit bounded 30 s timeout; lazy listing is bounded/partial. Native JS heap is not an OS RSS cap. Browser aggregate current/lifetime peaks remain diagnostics, not a whole-system pass. Actual hardware is i7-12700H/20 logical CPUs/15.73 GiB/Node26.5/SQLite3.53.3; reference 4-core hardware, cold GUI, long-term leak freedom, human/provider/production/commercial acceptance are not qualified.

Retained failures: baseline oversized startup and repeated graph reads; the initial 656/657 authority-contract failure; parser native stack exits; 100-object ERD 1969 ms; anchor/filter and mobile-heading bugs; incorrect aggregate RSS assertion; final P2 __proto__ dictionary RED. Each relevant product failure has a focused fix and current regression. A later ordinary sandbox run had lease/symlink denials (631 pass/16 fail/3 skip, one owned stalled test child terminated); its receipt is retained, and the authorized native repeat passed all 658. Attempt10 browser passed against the pre-promotion manifest; attempt11 is the current binding. No failed receipt was rewritten.

Docs: 26 domain Markdown files plus RU/EN matrix and four root control-plane files, 32 in total. Source registry RU/EN includes Context7 primary sources. Repaired a temporary helper's damaged G04 design block and registry heading before final source checks; original cards/AC remain preserved. EVALS/prod_test and diagram/MkDocs routes: no_change_needed, because no AI rubric, Batch39 or atlas/navigation contract changed. No site build/freshness claim. Cleanup removes owned fixtures and the copied test executable; existing cache/runtime and user files are preserved. Rollback only own hunks, followed by native requalification for executable source changes.

## FUNC-G05 — execution and decisions {#func-g05-results}

Status: implemented / locally_verified_with_explicit_limits,5/5. Scope F11/F12/F13/F15/F16. At task start HEAD8c2fbd4 and1120 source snapshots were captured; the only dirty file was the own lifecycle marker. Other29 task records, original AC/groups/M5 and G01–G04 receipts are preserved. Root integrated shared files; independently owned autonomy implementation and read-only source/design/review work used the documented ownership refinement. Current checks and claim limits follow below.

F11/F16 source gate: current selected App-agent bridge exposes local PAOS history, server-observed intervals and mediated operations; it has no host-history/model/effort/loaded-asset/token attestation port. Official App Server supports history/usage methods, which are a different capability and pinned-version admission boundary. No private host-store scrape, new API-key route or fabricated observations. Open/unresolved intervals remain unknown; separate task elapsed/agent effort and mediated commands/all host tools; tokens/cost remain unknown without a supported source. F12 external source and F15 extension contracts will be pinned before their build.

Code-change contract: existing_capability=F28 checked sources, LocalStore CAS, G04 fixed native lease, existing Team/Sessions/Artifact/Autonomy and V3 UI; smallest_safe_patch=route-aware projections and bounded adapters/writer, preserve unrelated routes; invariants=project/profile/root/policy isolation, raw source pins, idempotency, no invented attestation or metrics, no lost user edits; dependency_decision=no_new_dependency, installed/native capabilities first; risk_selected_tests=existing public HTTP/service/worker seams plus real synthetic native/browser conflict/recovery/isolation tests; comment_decision=comment_needed for authority, retention, journal and metric semantics; performance_applicability=required for bounded query/output/journal/fetch paths, no unrelated full F20 rerun; evidence_and_gaps=proceed with local source/synthetic evidence, host/provider/real-target acceptance separate.

F13 design gate: server-derived origin determines source-vs-SQL ownership. SQL document apply updates target, proposal and outcome in one Store CAS transaction. Workspace apply accepts only existing readable regular .md/.txt up to512KiB after F28 admission; AGENTS.md, SKILL.md, .codex/config/hooks/rules/plugin/skill instruction paths, ignored/generated/private/link/hardlink/reparse sources and redacted before/after are denied. Apply-preview binds project/profile/root/policy/epoch, proposal revision, raw before identity/hash and persisted after hash; final apply accepts neither client paths nor a replacement body. New proposals retain server-derived source pins; legacy proposals require refresh/restage. A fixed trusted Windows helper holds root→parent handles plus an exclusive existing-target handle, validates raw hash, waits for durable private prepared journal and final scope/policy fence, then writes/flushes/rehashes through that handle. This is protected in-place writing with recovery, not atomic replacement. A SQLite fence blocks policy/authority/cutover changes before writing; unresolved outcomes block new writes without replay. Current=after reconciles applied, current=before permits explicit retry, otherwise recovery_required without overwrite. Rollback requires a separate preview/current-hash CAS. Protected profile metadata journal is outside public document/settings snapshots: at most4 records/project,2MiB/record and8MiB/project; only terminal records may be evicted, unresolved records remain, quota fails closed. Public events/API expose metadata/hashes, no journal bytes. Existing readers/writers cause busy; user processes are never closed. Root control-plane documents except AGENTS require exact-file preview; source and SQL are never synchronized implicitly.

### F12 source gate before build

The deprecated openai/skills default was rejected in favor of the current public openai/plugins package superpowers, pinned to d420d13051bffe4543ed39e30fa46b87148e47dd (manifest6.3.0 and actual MIT LICENSE verified). This adapter searches only that explicit package, not the whole marketplace. Fixed anonymous api.github.com GETs traverse commit/root/plugins/package trees; no query/project context, credentials, redirects, foreign repositories, scripts/hooks/installation or provider calls. Limits:10s operation deadline,2MiB JSON/body,1000 package tree entries,256KiB SKILL,32 skill-local Markdown/text resources,1MiB bundle,15min catalog cache/four bundle cache entries. Blob bytes verify Git blob SHA separately from raw SHA256. Preview includes actual license/provenance and complete supported resources; links/submodules/outside-skill references/unknown licenses/executable or unsupported resources fail closed. Search never installs; managed copy uses existing preview/apply/CAS, including dependency checks and cached immutable source proof. Timeout/offline/rate limit never replaces or breaks local sources. Native plugin bindings remain unavailable and require owner compatibility review.


Live index inspection found agents/openai.yaml in every current skill, so the text-only subset was not useful. Before extending support, pin the exact exception: skill-local agents/openai.yaml is retained as opaque UTF-8 text, never parsed as executable host configuration or activated. All other unsupported resource rules remain; failed initial anonymous receipt is retained.

### FUNC-F15 — implementation boundary

Optional `maxCommandsTotal` limits durable command reservations across the policy window; omission preserves the v1 contract. Repeated operation IDs do not consume twice; uncertain outcomes do not refund reservations. The final admitted command may finish; subsequent commands/runs are denied. Reservations differ from F11 observed commands; tokens/cost and host tools remain unavailable and are not claimed to be constrained. Narrow allowedPaths retain their existing rejection. During F15 implementation the document_apply agent is the sole code writer for autonomy contracts/service/UI/tests; root handles documentation and read-only preparation.

Intermediate checkpoint before final qualification: F11 lifecycle/scope/recovery3/3; F12 source/negative cases3/3 and anonymous upstream8GET; F13 native13 cases (latest rollback regression1/1), pairedAPI1/1; F15 policy/runtime20/20; F16 identity/cursor2/2; cross-capability pairedAPI1/1. Independent source review found and verified the F13 rollback-operation fix. Native candidate and production-default qualification passed on adapter aa9c663dd1df54c6f47258234b5b9e9b5df6e0980e5ff58677e4403e30584bcc with zero provider/model/credential operations; final fullsuite/browser/status checks were pending at that checkpoint; see the closure result below.

<!-- FUNC-G05 ownership refinement: After read-only boundary review ownership is refined: the agent owns only autonomy contract/service/UI/tests, root owns team/history/metrics/dashboard. Files do not overlap; the full build/suite follows a shared freeze. -->

### Closure evidence

Five tasks implemented; group closed against local technical AC. Fullweb686/686,0fail/skip; typecheck/build passed; browser16/16 (.tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json); native candidate→qualified default passed, adapter aa9c663dd1df54c6f47258234b5b9e9b5df6e0980e5ff58677e4403e30584bcc. Earlier actual RED/setup/selector receipts are retained; no failure is relabelled as a passed attempt.

Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG updated; EVALS=no_change_needed (no model/prompt/route/rubric changes); prod_test=no_change_needed (Batch39 ledger unchanged); atlas/navigation=no_change_needed (existing lifecycle boundaries, no new docs page/workflow). Root size advisories predate this slice; docs-maintainer owns a separate preservation-safe compactness follow-up. Git/publication/install/provider/real-profile operations absent. Final independent evidence review and preservation gates are recorded in latest verification.

Status audit: corrected the inherited RU overview M5 count, which had repeated FUNC totals. The current owning M5 JSON confirms56 cards,53 implemented/3planned; its content and statuses are unchanged.

Independent final review: context_mode=separate_reused_context; reviewer=/root/func_g05_completion_review; tester_verdict=closed_allowed; closure_level=locally_verified_with_explicit_limits. Evidence .tmp/func-g05/final-review.json, closure-consistency.json, docs-final.log (28sources), matrix-ru.log, matrix-en.log. Independently recomputed source/build/native hashes match; no open implementation/evidence blockers. Two expected SESSION_REQUIRED bootstrap401 responses are retained, with no unexpected HTTP/page errors or external browser requests. Parent Node peak237100KiB is not an aggregate OS memory measurement.

## FUNC-G06 — execution and decisions {#func-g06-results}

Status: implemented / locally_verified_with_explicit_limits,3/3. At start HEADade8e4c and1159 snapshots were recorded; only own marker was dirty. Other31 tasks, immutable AC/groups/order/M5 and G01–G05 receipts are preserved. The design gate below preceded implementation; current evidence and limits follow.

Code-change contract: existing_capability=durable recipe checkpoints/scheduler ownership, migration freeze/CAS, SQL/blob snapshots, portable content-addressed package and profile-maintenance reservations; smallest_safe_patch=distinct crash/import/recovery qualification and managed local delivery orchestration atop existing helpers, no framework rewrite; invariants=source/destination/profile identity, one writable authority, no replay/duplicates, no credential/approval revival, preserve old versions/profiles and unrelated dirty work; dependency_decision=no_new_dependency; risk_selected_tests=public APIs/CLI and owned child-process/native synthetic seams, independent counts/hashes/FK/blob oracles; comment_decision=comment_needed for recovery/admission/journal invariants; performance_applicability=required for bounded copies/process deadlines, no unrelated scale benchmark; evidence_and_gaps=proceed_with_local_synthetic, distribution design must precede build, real installation/signing/publication/new OS account/provider acceptance separate.

### F17 — delivery decision

F17 design gate (before build): private_local_pilot channel; managed user-space installer over the existing portable directory using Node CLI setup/update/rollback and one managed-home. Unsigned, separately verified releaseId; SHA256 is integrity, not publisher authentication. Existing exact Node/Windows/SQLite prerequisites, AUTH-G1–G6/licensing/public/commercial gates remain separate. Fresh Windows-profile acceptance means a new disposable PAOS profile plus fresh USERPROFILE/HOME/APPDATA/LOCALAPPDATA/TEMP/CODEX_HOME in a child process on the existing Windows account. A new OS account/SID, system installation, SmartScreen/signature trust and human acceptance are not claimed. Current-profile maintenance must span backup→restore→selection (or an under-lease DB+WAL freshness CAS); tuple admission precedes selection. Keep all old profiles/versions/backups; interrupted operation remains explicit/fenced, no silent replay or checkout fallback. Architect audit: /root/func_g06_distribution_design, read-only; existing helpers reused, no new dependencies.

Intermediate checkpoint before F17 implementation: F21 qualification:20/20 (.tmp/func-g06/f21-focused-final.log); F22 qualification:11/11 (.tmp/func-g06/f22-focused.log). Characterization tests validate existing production behavior; no artificial RED or unrelated product change. At that checkpoint F17 build dependency was satisfied; implementation and combined qualification were completed afterward.

### Closure evidence

F21:20/20, real process crashes before dispatch / in-flight without receipt / terminal receipt; F22:11/11, interrupted promotion retry + independent FK negative; fullweb694/694,0fail/skip; managed package10/10 (.tmp/func-g06/managed-acceptance/evidence-mJ8j5k/result.json); typecheck/build/native candidate→default passed. Current adapter ab195406a2f961c55d90d3a1848d4bcd98b644f10c66da7085cde94d0f584f51. Three actual installed phases A/B/A with distinct profiles and exact served HTML hashes, actual launcher IPC/service, fresh global home canary, public task/comment/blob/preferences and trusted offline installed-Store chat fixture preparation followed by public readback. No serviceModule/inspectRuntime replacement. Three expected bootstrap401 retained; no unexpected HTTP/page/external errors.

Private unsigned user-space delivery on the existing Windows account; no new OS account/SID, actual native GUI/SmartScreen, system installation, signing/commercial/public release, provider/model or human acceptance. Cooperative managed profile reservations do not sandbox arbitrary SQLite writers. Every original file hash is preserved; explicitly recorded new empty WAL/32KiB SHM bookkeeping means whole-directory identity is not claimed. Rollback restores the explicitly selected compatible snapshot; newer work needs a fresh compatible backup.

Retained failures: missing managed CLI and fresh-home propagation actual RED; independent review home-lock fence actual RED→GREEN; first acceptance seed hit USER_WRITE_FORBIDDEN; whole-inventory assertion exposed new SQLite sidecars. Source code was not weakened to satisfy fixture/oracle setup. Intermediate9/9 pass precedes added schema-negative; final10/10 includes a self-consistent incompatible-schema manifest and unchanged selection.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG updated; EVALS=no_change_needed (model/prompt/agent-behavior/rubric unchanged); prod_test=no_change_needed (Batch39 ledger unchanged); atlas/navigation=no_change_needed (existing runtime boundaries, no new docs page). Existing root compactness advisories remain a separate docs-maintainer follow-up with preservation. Final independent review/preservation/static gates own parent closure.

Independent final review: context_mode=separate_reused_context; reviewer=/root/func_g06_completion_review; tester_verdict=closed_allowed; closure_level=locally_verified_with_explicit_limits. Evidence: .tmp/func-g06/final-review.json, closure-consistency.json, docs-final.log(14sources), matrix-ru.log/matrix-en.log(ok=true,errors=[]). Initial failed validator receipts are retained as matrix-ru-pre-repair.log/matrix-en-pre-repair.log; source/package/dist inputs are unchanged after metadata repair. No open implementation/evidence blockers.

## Detailed cards

### Task `PAOS-FUNC-01`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-01 — Restore native runtime qualification after the redesign
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:17
- Priority: P1
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-08`, `PAOS-FUNC-10`, `PAOS-FUNC-15`, `PAOS-FUNC-16`, `PAOS-FUNC-17`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-21`, `PAOS-FUNC-22`
- Source: Lock SHA-256 d279009a… in the manifest and f126e4dc… in the current file did not match; adapter99 matched in the 15.11 audit. [packages/contracts/runtime/manifest.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/runtime/manifest.mts), [apps/local-service/src/runtime/sandbox-broker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/sandbox-broker.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Restore native runtime qualification after the redesign.
- Technical value: Align lockfile, manifest and native broker without weakening the fingerprint check.
- Product value: Starting a task from the redesigned UI actually results in execution.
- Scope: `packages/contracts/runtime/manifest.mts`; `packages/contracts/runtime/qualified-manifest.json`; `apps/local-service/src/runtime/sandbox-broker.mts`; `tests/web/runtime-manifest.test.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people's dirty changes are outside the fix.
- Expected result: Starting a task from the redesigned UI actually results in execution. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Reproduce package_lock_mismatch with the current lockfile; the fix must not substitute a simple hash overwrite for qualification. AC2: On a newly qualified tuple, the new broker executes a synthetic command within the permitted root and rejects writes outside it. AC3: Negative scenarios for changed binary, lockfile and adapter remain fail-closed; restart passes.
- Verification gates: `node --test tests/web/runtime-manifest.test.mts` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: native_synthetic_acceptance_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 8–16 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: plugin-runtime-builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group's JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Reproduced package_lock_mismatch; candidate-only qualification admits changed lock/adapter pins solely for new native acceptance. Promoted manifest only after a passed native receipt; production loader remains fail-closed.
- files touched / work locations: `packages/contracts/runtime/qualified-manifest.json`, `tests/web/runtime-manifest.test.mts`, `tests/web/single-window/sandbox-broker-acceptance.mts`
- technical value delivered: Current lockfile qualified with binary/Node/OS/SQLite and adapter; drift protections preserved.
- product value delivered: A new native broker executes a synthetic command inside its allowed root and denies outside writes.
- actual implementation date and time: 15-11-2026 18:17
- verification evidence: RED `.tmp/func-g01-runtime/manifest-red.log`, `native-red.log`; GREEN runtime-manifest + sandbox-broker 12/12; native candidate/default `.tmp/func-g01-runtime/native-candidate-initial-escalated.log`, `native-default-initial-escalated.log` exit0, three modes, inside write/outside+temp EPERM, binary/lock/adapter drift rejected before spawn, repeat start/Stop/auth cleanup. Initial sandbox MXC failure retained in native-candidate-initial.log. Final F08 requalification: `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, `native-default-final-escalated.log` exit0; adapter fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5, lock f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac; runtime12/12. Binary cleanup verified.
- residual risks: Bounded native offline acceptance; no provider/model/production/human acceptance claim. Final tuple after F08 verified.
- follow-up: None within these AC; any new pinned-source edit requires new qualification.
- Documentation impact: updated; `docs/backend/lifecycle.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Documents the exact tuple, candidate promotion, current receipts and claim boundary.

### Task `PAOS-FUNC-02`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-02 — Restore links between structured artifacts and tasks
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-13`, `PAOS-FUNC-14`, `PAOS-FUNC-19`
- Source: taskPaths reads files/artifactReferences; Editor saves artifacts separately. [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/web/src/features/tasks/Editor.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/Editor.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Restore links between structured artifacts and tasks.
- Technical value: Unify normalization of files, artifactReferences, artifacts and fileContexts.
- Product value: A document can be found from its task, and a task from the document and search.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/impact/service.mts`; `tests/web/skill-generation-artifacts.test.mts`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people's dirty changes are outside the fix.
- Expected result: A document can be found from its task, and a task from the document and search. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: A task referenced only in artifacts.reference is found by the catalog taskId filter and displayed among the document's linked tasks. AC2: Legacy artifactReferences/files preserve behavior; duplicates and path separators are normalized. AC3: External URLs are not treated as local paths; stale revision and unavailable file are shown explicitly. AC4: File references use F28 normalization and root identity; catalog, tree and tasks point to the same permitted relativePath/revision. Deleted/moved/excluded does not become an accessible document or read permission.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts` These are future task checks, not checks performed by this planning. First reproduce RED on the current version, then fix and GREEN. General docs gates apply when documentation changes.
- Risks / approval gates: reproduce_then_fix; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 4–8 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group's JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Next step: Complete F29/F10/F18 and final FUNC-G03 gates.

#### Completion Report

- status: implemented
- what was done: Shared explicit task-reference normalization connects structured artifacts and legacy paths with catalog/backlinks; stale pins remain separate from current document availability and read authority.
- files touched / work locations: apps/local-service/src/artifacts/references.mts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/task-manager/service.mts; apps/web/src/features/artifacts/ArtifactExplorer.tsx; tests/web/skill-generation-artifacts.test.mts
- technical value delivered: Registry/root/policy/revision contracts verified through actual HTTP/SQLite/FS and production React.
- product value delivered: Project sources are available with explicit unavailable reasons and preserved navigation.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0; .tmp/func-g03/f02-focused-final.log:21/21
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Complete F29/F10/F18 and final FUNC-G03 gates.
- Documentation impact: updated; docs/code-intelligence/queries-impact.md; docs/code-intelligence/queries-impact.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-03`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-03 — Fully reset the new-task draft
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:26
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-19`
- Source: Reset does not clear rawInputs; the clearing effect requires an entity. [apps/web/src/features/tasks/Editor.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/Editor.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Fully reset the new-task draft.
- Technical value: Synchronize model, rawInputs, estimate, preview and dirty-state on Discard.
- Product value: After cancellation, the user does not see data already absent from the saved task.
- Scope: `apps/web/src/features/tasks/Editor.tsx`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: After cancellation, the user does not see data already absent from the saved task. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Populate criteria/risks/references/estimate in a new task and press Discard: all fields and model return to the same empty state. AC2: The next save does not restore discarded data; dirty/preview/error states are not misleading. AC3: For an existing task, Discard restores the server revision and does not destroy another user's changes.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: browser_reproduction_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 3–6 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Discard clears rawInputs, reason/error, model, estimate, preview and dirty-state. Saving after discard does not resurrect data; conflicts retain dirty input, discard adopts the current server revision.
- files touched / work locations: `apps/web/src/features/tasks/Editor.tsx`, `tests/web/single-window/func-g01-drafts-acceptance.mts`
- technical value delivered: Discard clears rawInputs, reason/error, model, estimate, preview and dirty-state. Saving after discard does not resurrect data; conflicts retain dirty input, discard adopts the current server revision.
- product value delivered: Discard predictably resets the form without silently losing concurrent edits.
- actual implementation date and time: 15-11-2026 18:26
- verification evidence: Baseline RED `.tmp/func-g01-drafts/evidence-DGhYbl/result.json`; ACK-race RED evidence-pS0YXr/result.json; final `.tmp/func-g01-drafts/evidence-C6lIVM/result.json` 54/54 on final F08 build, actual UI/HTTP/SQLite concurrent writes, source/build hashes, fixture cleanup; typecheck exit0. Retained sandbox startup and premature-oracle receipts3Hhk34/8nW2Uj/W7ljj0; bounded observable waits repaired test timing.
- residual risks: Browser desktop/mobile geometry checked; human acceptance and full UX/a11y qualification remain separate. Drafts remain page-memory only.
- follow-up: None within these AC; end-to-end F19 and human F23 remain planned.
- Documentation impact: updated; `docs/frontend/state-management.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Separate F03/F04 sections document reset/navigation/CAS, current source ownership and 54-check evidence.

### Task `PAOS-FUNC-04`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-04 — Preserve workflow assignment drafts during navigation
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:26
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-19`
- Source: Draft cache does not include typeMapping/mappingDirty. [apps/web/src/features/workflows/WorkflowManager.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/workflows/WorkflowManager.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Preserve workflow assignment drafts during navigation.
- Technical value: Include typeMapping and original CAS revision in the shared draft lifecycle.
- Product value: The user does not lose unsaved process assignments when navigating between sections.
- Scope: `apps/web/src/features/workflows/WorkflowManager.tsx`; `tests/web/single-window/m2b-browser-acceptance.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The user does not lose unsaved process assignments when navigating between sections. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Change task-type mapping, leave Settings and return: the draft is restored or navigation is stopped beforehand with a clear choice. AC2: Save/Discard correctly clear dirty-state; default workflow and mapping do not overwrite each other. AC3: Switching projects does not transfer the draft into another project; a stale save returns conflict without losing the input.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: browser_reproduction_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 4–8 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Memory-only drafts retain typeMapping/mappingDirty/original CAS revision independently of definitions. Navigation/project changes are isolated; Save/Discard assignments work; a default-only ACK adopts only its own committed revision, never another writer from refresh.
- files touched / work locations: `apps/web/src/features/workflows/WorkflowManager.tsx`, `tests/web/single-window/func-g01-drafts-acceptance.mts`
- technical value delivered: Memory-only drafts retain typeMapping/mappingDirty/original CAS revision independently of definitions. Navigation/project changes are isolated; Save/Discard assignments work; a default-only ACK adopts only its own committed revision, never another writer from refresh.
- product value delivered: Unsaved assignments survive navigation without overwriting another writer.
- actual implementation date and time: 15-11-2026 18:26
- verification evidence: Baseline RED `.tmp/func-g01-drafts/evidence-DGhYbl/result.json`; ACK-race RED evidence-pS0YXr/result.json; final `.tmp/func-g01-drafts/evidence-C6lIVM/result.json` 54/54 on final F08 build, actual UI/HTTP/SQLite concurrent writes, source/build hashes, fixture cleanup; typecheck exit0. Retained sandbox startup and premature-oracle receipts3Hhk34/8nW2Uj/W7ljj0; bounded observable waits repaired test timing.
- residual risks: Browser desktop/mobile geometry checked; human acceptance and full UX/a11y qualification remain separate. Drafts remain page-memory only.
- follow-up: None within these AC; end-to-end F19 and human F23 remain planned.
- Documentation impact: updated; `docs/frontend/state-management.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Separate F03/F04 sections document reset/navigation/CAS, current source ownership and 54-check evidence.

### Task `PAOS-FUNC-05`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-05 — Show incomplete portfolio coverage next to totals
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-11`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: aggregateSnapshots returns partial; dashboard totals do not display it. [apps/web/src/features/dashboard/model.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/model.ts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Show incomplete portfolio coverage next to totals.
- Technical value: Pass partial/loaded/expected from the aggregator into KPI and progress displays.
- Product value: Partially loaded projects do not look like a complete portfolio total.
- Scope: `apps/web/src/features/dashboard/model.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Partially loaded projects do not look like a complete portfolio total. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: With one successful and one failed project, show “1 of 2; incomplete data” next to totals. AC2: Unknown values are not replaced with zero; progress explicitly refers to the available sample. AC3: Loading, retry, all-failed and restoration of full coverage are checked in RU/EN.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: reproduce_then_fix; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 3–6 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Displayed loaded/expected and partial next to totals/progress; expected count comes from projects before the first response.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`, `apps/web/src/design/parity.css`
- technical value delivered: Displayed loaded/expected and partial next to totals/progress; expected count comes from projects before the first response.
- product value delivered: Partial portfolio totals are visibly incomplete; unknown is not zero.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures for failures/timestamps/queue; no provider/human acceptance or full accessibility qualification claim.
- follow-up: None within these AC; end-to-end F19/F24 remains separate.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Documents current display rules, source owners and browser evidence.

### Task `PAOS-FUNC-06`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-06 — Correct dashboard queue numbering
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P3
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-19`
- Source: Backend uses indexOf+1, dashboard uses position+1. [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Correct dashboard queue numbering.
- Technical value: One 1-based position contract between scheduler and frontend.
- Product value: Tasks have the same order on the dashboard and in queue management.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Tasks have the same order on the dashboard and in queue management. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Backend positions 1/2 appear as #1/#2 on the dashboard. AC2: A null position shows no number; reorder is reflected consistently on both surfaces.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: reproduce_then_fix; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 1–3 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Removed the extra +1 from scheduler position; null has no number.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`
- technical value delivered: Removed the extra +1 from scheduler position; null has no number.
- product value delivered: Dashboard and QueueManager show consistent positions and reorder.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures for failures/timestamps/queue; no provider/human acceptance or full accessibility qualification claim.
- follow-up: None within these AC; end-to-end F19/F24 remains separate.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Documents current display rules, source owners and browser evidence.

### Task `PAOS-FUNC-07`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-07 — Sort recent tasks by time
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Defect; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P3
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-18`, `PAOS-FUNC-19`
- Source: Dashboard uses slice(-3), storage uses ORDER BY id. [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Sort recent tasks by time.
- Technical value: Define explicit updatedAt sorting with stable tie-breaker and unknown policy.
- Product value: The recent-task block leads to genuinely recent work.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `tests/web/ui-v3-dashboard.test.mts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The recent-task block leads to genuinely recent work. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: UUID order is deliberately opposite to time: the 3 most recent by updatedAt are displayed. AC2: Equal and missing timestamps are handled deterministically; the label explains the selected semantics. AC3: Creating and changing a task updates the block after refresh.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Executed commands, RED/GREEN and provenance are recorded in the Completion Report.
- Risks / approval gates: reproduce_then_fix; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 2–4 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Added pure updatedAt sorting, ID tie-breaker and unknown-last ordering; the UI explains the semantics.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`
- technical value delivered: Added pure updatedAt sorting, ID tie-breaker and unknown-last ordering; the UI explains the semantics.
- product value delivered: The three recent tasks reflect creation and edits after refresh.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures for failures/timestamps/queue; no provider/human acceptance or full accessibility qualification claim.
- follow-up: None within these AC; end-to-end F19/F24 remains separate.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Documents current display rules, source owners and browser evidence.

### Task `PAOS-FUNC-08`

- Delivery group: `FUNC-G01`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-08 — Separate shared contracts and UI/backend dependencies
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Architecture; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:27
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-09`, `PAOS-FUNC-11`, `PAOS-FUNC-13`
- Source: HTTP imports web/preferences; contracts imports local-service/task-profile. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [packages/contracts/issues/task-profile.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/issues/task-profile.ts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Separate shared contracts and UI/backend dependencies.
- Technical value: Remove backend→frontend and contracts→backend imports while preserving public behavior.
- Product value: Appearance changes are less likely to break server functions and delivery.
- Scope: `apps/local-service/src/http/application.mts`; `apps/web/src/design/preferences.ts`; `packages/contracts/issues/task-profile.ts`; `apps/local-service/src/tasks/task-profile.ts`. Completed-slice ownership: root + assigned agents; shared edits serialized.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Appearance changes are less likely to break server functions and delivery. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Preferences and task decoder have one independent owner; contracts do not import apps. AC2: Existing payload/schema and failure scenarios are preserved; frontend and service pass typecheck and current tests. AC3: An import-direction check prevents regression; runtime tuple is requalified if pinned sources are affected.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` These are future task checks, not checks performed by this planning. Preserve current contracts, check regressions and compare before/after. General docs gates apply when documentation changes.
- Risks / approval gates: architecture_review_before_refactor; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Closed against local AC; changed pinned sources require requalification.

#### Completion Report

- status: implemented
- what was done: Moved two pure implementations into independent contract ownership. M1 decoder bytes are preserved except the import; legacy paths re-export the same functions. DOM apply stays in Web. AST guard covers import/export/type/literal dynamic edges; HTTP payload/schema unchanged.
- files touched / work locations: `packages/contracts/tasks/decode-task-profile.ts`, `packages/contracts/ui/preferences.ts`, legacy decoder/frontend preferences re-exports, `issues/task-profile.ts`, HTTP `application.mts`, `locales/messages.ts`, `tests/web/contracts-boundaries.test.mts`, final runtime manifest
- technical value delivered: Removed contracts→apps and service→Web-source reverse imports without new dependencies or validation rewrites.
- product value delivered: Appearance changes no longer require importing frontend implementation into backend preferences.
- actual implementation date and time: 15-11-2026 18:27
- verification evidence: Independent pre-edit architecture review /root/func_g01_runtime; AST RED found exact contracts-to-service + service-to-Web edges; GREEN shared/decoder/M2/preferences focused15, npm run check:web-m1/build:web exit0. Final native candidate/default exit0 `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, native-default-final-escalated.log; manifest adapter fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5; runtime12/12. Full Web `.tmp/func-g01/web-final.log` 507 tests492pass/11fixture EPERM/4skip + exact15 boundary retests `.tmp/func-g01/web-boundary-retest.log`15pass0fail0skip:507 unique passed across two executor contexts. Independent final review /root/func_g01_review closed_allowed.
- residual risks: Existing Web package/parser packaging dependency remains. The AST guard covers static/literal edges, not arbitrary computed imports; no increased provider/human/production claim.
- follow-up: None within these AC; a new pinned-source edit requires native requalification.
- Documentation impact: updated; `docs/backend/modules.md` + `.en.md`, `docs/architecture/containers.md` + `.en.md`, `docs/sources/registry.md` + `.en.md`; Documents ownership, compatibility seams, decision/alternative and final qualification. API docs no_change_needed: endpoints/payload/schema/errors preserved.

### Task `PAOS-FUNC-09`

- Delivery group: `FUNC-G04`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-09 — Optimize snapshot reads and lifecycle
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Architecture; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-08`, `PAOS-FUNC-20`
- Blocks: `PAOS-FUNC-14`
- Source: Full projectEntities; graph memory cap 8; catalog snapshot limits. [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/local-service/src/task-manager/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/task-manager/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Optimize snapshot reads and lifecycle.
- Technical value: Eliminate measured redundant full scans and add bounded cache release.
- Product value: Long-running work and large projects are not hindered by delays and accumulated snapshots.
- Scope: `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/sessions/service.mts`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Long-running work and large projects are not hindered by delays and accumulated snapshots. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Select and implement only bottlenecks reproduced by F20; before/after uses the same workload. AC2: The ninth project does not require restart solely due to 8 graph snapshots: eviction/rebuild preserves revision/cursor safety. AC3: Task/artifact/history read load is bounded; exceeding budget yields explainable partial/error and safe recovery. AC4: After F20 compare metadata listing, graph status and scanner on the same workload: a repeated status query must not unconditionally reread all file contents; bytes/read and scan count are measured. AC5: Cache key/eviction accounts for root identity, policy version and F27/F28 scan revision; eviction does not hide files from the F26 tree or mix projects.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` These are future task checks, not checks performed by this planning. Preserve current contracts, check regressions and compare before/after. General docs gates apply when documentation changes.
- Risks / approval gates: measured_bottleneck_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 12–24 h after benchmark; rough_range_not_commitment. Refine on the current build before starting.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Next step: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.

#### Completion Report

- status: implemented
- what was done: Implemented measured F20 fixes: metadata-only graph status,8-entry LRU/generation-bound cursors,8 checked parallel source handles with unchanged8MiB cap, SQL kind filtering before64MiB cap, frozen TEMP history and SQL artifact previews with bounded raw reads.
- files touched / work locations: apps/local-service/src/code-index/service.mts; apps/local-service/src/storage/; apps/local-service/src/sessions/service.mts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/main.mts; tests/web/snapshot-lifecycle.test.mts; tests/web/snapshot-history-scale.test.mts
- technical value delivered: Removed startup SNAPSHOT_TOO_LARGE, repeated body reads on status and ninth-project refusal while preserving raw SHA256/authority guards and immutable history.
- product value delivered: Large history/documents do not block task reads; eviction requires no restart and never hides Files.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; observable RED3/3→GREEN3/3 plus real100k-message frozen/1000-large-document regressions; full658 includes current guards; Baseline graph 60.865 s/status 17.6–21.3 s/ninth LIMIT; current closure graph 11475.70 ms/status 313.49/294.86/277.69 ms, 0 content reads/bytes and one metadata walk; ninth project succeeds; final cold-generation deviations and fast existing cursors retained in F20 receipts; no threshold raised
- residual risks: A new large cold snapshot does not meet the1s warm SLO; partial/recovery and230MiB payload/256MiB TEMP caps remain. History expiry15min/eviction/restart requires refresh. Status checks metadata; excerpts verify raw hashes. JS heap does not cap native RSS.
- follow-up: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.
- Documentation impact: updated; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/backend/lifecycle.md; docs/backend/lifecycle.en.md; docs/db/transactions.md; docs/db/transactions.en.md; docs/testing/test-map.md; docs/testing/test-map.en.md; scoped source checks passed.

### Task `PAOS-FUNC-10`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-10 — Show file-scope limitations before execution
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Improvement; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-15`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: Capture is limited to 32 files, 64KiB/file, 512KiB total. [apps/local-service/src/runtime/app-agent-files.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-files.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Show file-scope limitations before execution.
- Technical value: Shared preflight for file count, sizes, excluded paths and actual-diff boundaries.
- Product value: The user understands in advance why a task cannot start and how to split it.
- Scope: `apps/local-service/src/runtime/app-agent-files.mts`; `apps/local-service/src/runtime/app-agent-gateway.mts`; `apps/web/src/ui/SessionContext.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/files/ProjectFiles.tsx` (new planned file). Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The user understands in advance why a task cannot start and how to split it. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Check 32/33 files, 64KiB/64KiB+1 and total 512KiB before dispatch with a specific explanation. AC2: Sensitive/link/binary exclusions do not reveal contents; blocked execution is not presented as a started run. AC3: Any required limit increase passes a separate bounded performance/security gate; limits are not removed unconditionally. AC4: A file reference selected from the F26 tree undergoes execution preflight again: visibility/readability/indexing does not authorize dispatch. Show F28 policy and actual execution limits separately; stale path/root requires refresh.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: shared_preflight_contract_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 6–12 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Next step: No remaining work in this task; future consumers/packaging/performance retain their own tasks.

#### Completion Report

- status: implemented
- what was done: One metadata-only preflight checks saved scope, original32/64KiB/512KiB budgets, operations/rename/pins/policy/root before Send; the server repeats authority checks and native dispatch rechecks policy after waits. Blocked UI retains its draft and creates no run.
- files touched / work locations: apps/local-service/src/runtime/app-agent-files.mts; apps/local-service/src/runtime/task-file-preflight.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts; apps/web/src/ui/SessionContext.tsx; apps/web/src/ui/App.tsx; tests/web/file-preflight.test.mts
- technical value delivered: Shared root/policy/revision contracts and final authority fences verified on current API/SQLite/FS/build/native fixtures.
- product value delivered: Partial and stale observations are explicit; execution limits are explained before dispatch while source data and drafts are preserved.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: No remaining work in this task; future consumers/packaging/performance retain their own tasks.
- Documentation impact: updated; docs/security/filesystem.md; docs/security/filesystem.en.md; docs/db/transactions.md; docs/db/transactions.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-11`

- Delivery group: `FUNC-G05`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-11 — Introduce measurable run and consumption statistics
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-08`
- Blocks: `PAOS-FUNC-15`
- Source: Metrics durationSeconds/tokenCount/cost=null; tool_use is not measured. [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Introduce measurable run and consumption statistics.
- Technical value: Versioned telemetry with provenance, deduplication and session→run→task→agent aggregation.
- Product value: Duration and consumption help compare work without invented numbers.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/events/task-time.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: Duration and consumption help compare work without invented numbers. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: First approve available duration/tokens/tool calls/cost sources, privacy and retention; unsupported fields remain unknown. AC2: Event replay does not increase totals; partial streams, restart and links to multiple agents do not cause double counting. AC3: Dashboard, task and agent show consistent values, period and source; cost appears only with a known calculation model.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/task-time.test.mts tests/web/ui-v3-dashboard.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: telemetry_source_privacy_design_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h discovery/design; build after source selection; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: telemetry_source_privacy_design_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

#### Completion report

- status: implemented
- what was done: Versioned numeric telemetry measures run intervals and mediated commands, excludes approval waits, deduplicates retries and preserves unknown values on recovery. One scoped endpoint and RunUsage show consistent values across Dashboard/project/task/session/agent; tokens/cost/host tools remain unknown.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/llm/budgets-and-observability.en.md; docs/api/endpoints.en.md; docs/frontend/components.en.md; docs/security/data-retention.en.md; registry and scoped source checks.

### Task `PAOS-FUNC-12`

- Delivery group: `FUNC-G05`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-12 — Design and connect external skills search
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: none
- Blocks: none
- Source: remote_discovery_adapter_not_configured. [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Design and connect external skills search.
- Technical value: Separate read-only discovery adapter with provenance, license, pin and preview.
- Product value: A suitable skill can be found outside the local catalog and added with an informed decision.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/team/sources.mts`; `apps/web/src/features/team/TeamManager.tsx`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: A suitable skill can be found outside the local catalog and added with an informed decision. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build choose a permitted source, network/privacy policy and result format. AC2: Search shows origin/license/revision; timeout/offline does not break the local catalog. AC3: Search installs nothing; adding uses existing preview/apply and checks drift and dependencies.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-review-repair.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: external_source_design_and_authority_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 4–8 h design; build after adapter selection; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: external_source_design_and_authority_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

#### Completion report

- status: implemented
- what was done: Explicit anonymous fixed-source discovery for pinned openai/plugins superpowers checks Git/raw hashes, actual MIT license and path/mode/dependency/byte/deadline limits. Queries stay local; preview→Apply creates a managed copy with resources/provenance/license without native activation. External failures preserve the local catalog.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/security/supply-chain.en.md; docs/api/endpoints.en.md; docs/frontend/components.en.md; docs/product/capabilities.en.md; registry and scoped source checks.

### Task `PAOS-FUNC-13`

- Delivery group: `FUNC-G05`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-13 — Add safe application of document proposals
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-08`
- Blocks: none
- Source: Current policy is staged_only, applied:false. [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Add safe application of document proposals.
- Technical value: Preview-bound compare-and-swap writer preserving user changes and recovery.
- Product value: An agreed proposal can be applied to a document within the app.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/http/application.mts`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: An agreed proposal can be applied to a document within the app. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build approve writer authority, source-vs-SQL ownership and eligible documents. AC2: Apply changes only the checked file when revision matches; an external edit causes conflict without overwrite. AC3: Repeated apply is idempotent; crash/rollback and sensitive paths are tested; staged/applied/accepted are shown separately.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts`; `npm run check:web-m1` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: document_write_authority_design_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h design; build after write contract approval; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: document_write_authority_design_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

#### Completion report

- status: implemented
- what was done: Preview/ack/CAS Apply, exact-current-preview rollback and explicit recovery support SQL and existing admitted Windows files. A protected durable journal, immutable outcome receipts, exclusive native handle/root pins, raw hash/file revision and bounded retention preserve bytes and unknown outcomes. Current rollback operation identity is fixed; writes do not create acceptance.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/db/transactions.en.md; docs/backend/recovery.en.md; docs/security/filesystem.en.md; docs/security/data-retention.en.md; docs/ai/llm/prompts-and-outputs.en.md; docs/frontend/components.en.md; docs/api/endpoints.en.md; registry and scoped source checks.

### Task `PAOS-FUNC-14`

- Delivery group: `FUNC-G04`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-14 — Improve usefulness and resilience of the project map
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-09`, `PAOS-FUNC-27`, `PAOS-FUNC-28`, `PAOS-FUNC-30`, `PAOS-FUNC-31`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`, `PAOS-FUNC-34`
- Source: lexical_subset_only, imports unresolved, memory-only index. [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Improve usefulness and resilience of the project map.
- Technical value: Choose language/relation support; durable revision index, imports resolution and honest coverage.
- Product value: The map helps assess change impact without giving the appearance of complete analysis.
- Scope: `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/code-index/lexical.mts`; `apps/local-service/src/impact/service.mts`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: The map helps assess change impact without giving the appearance of complete analysis. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build approve supported language/relation-type matrix; unsupported semantics remain explicitly marked. AC2: Within selected scope test cross-file imports/aliases on ground-truth fixtures; unresolved does not become a false edge. AC3: Restart/rebuild preserves or explicitly invalidates revision; D3/Mermaid/list and impact show one data set. AC4: The graph consumer uses F28 inventory and F27 code stage; discovered/readable/indexed/unsupported/excluded/error are distinct. An empty or successful JS/TS index does not imply complete project analysis. AC5: Graph ready/stale/unavailable does not block the F26 tree; restart/cancel/retry do not publish stale results, an unavailable parser leaves other scan results accessible. AC6: Record backend/composition and rollback selection from F30/F31; a justified PoC rejection is not a hidden fallback. Unsupported languages and semantics are explicit; a third-party engine's raw SQLite does not become the PAOS API. AC7: In the existing Map implement dependency/symbol modes within selected capabilities, search, incoming/outgoing, path/impact and an evidence drawer with file/line navigation. Graph/list/Mermaid, filters and counters use one snapshot; loading/empty/partial/error/unavailable/stale and version/coverage are visible. AC8: Apply the shared F30–F34 UI/UX contract to the production screen, not only the PoC; test Files↔Map navigation and project selection. Architecture is included only for a source-backed model: import is not a call, and C4 grouping is not an extracted business fact.
- Verification gates: `npm run test:web-m1`; `node --test tests/web/ui-v3-diagram.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: language_semantics_storage_design_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h design; build after language selection; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + graph-cockpit-engineer + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.

#### Completion Report

- status: implemented
- what was done: Selected an explicit installed-parser/pure-allowlist-resolver composition; added aliases/baseUrl, literal dynamic imports/unshadowed require, dependency/symbol modes, direction/bounded paths and source evidence→Files with one graph/list/Mermaid revision. Native parsing is contained in an owned child/watchdog.
- files touched / work locations: apps/local-service/src/code-index/; apps/local-service/src/process/child-watchdog.mts; packages/contracts/graph/code-graph.ts; apps/web/src/features/graph/; apps/web/src/ui/App.tsx; tests/web/graph-imports.test.mts; tests/web/graph-query-modes.test.mts; tests/web/graph-parser-isolation.test.mts
- technical value delivered: Ground truth imports10/10 without fake cross-file calls; unsupported/dynamic/unresolved and parser failures stay explicit, and Files remains independent.
- product value delivered: Map locates dependencies and source file/line with inspectable evidence and an accessible list.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; G02 corpus7/10→10/10 imports,fixture precision1/recall1; aliases/config drift/shadowing/cycles/Unicode/no config execution; native deep input failure contained; graph owner remains usable; actual child timeout/cancel cleanup; actual browser dependencies/direction/path/keyboard/source/Files and fresh nonempty Map in4locale/theme×2viewport states
- residual risks: JS/TS lexical/import subset only; no package exports/config inheritance/full TS linker/runtime calls or invented C4 facts. Restart/eviction requires rebuild.1k files/8MiB/512KiB and8-hop/1000-visited path limits remain.
- follow-up: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.
- Documentation impact: updated; docs/code-intelligence/graph-model.md; docs/code-intelligence/graph-model.en.md; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/backend/modules.md; docs/backend/modules.en.md; scoped source checks passed.

### Task `PAOS-FUNC-15`

- Delivery group: `FUNC-G05`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-15 — Clarify and extend autonomy boundaries
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-10`, `PAOS-FUNC-11`
- Blocks: none
- Source: Executable scope is only '.', hostToolsConstrained=false, tokenCostMetering unavailable. [apps/local-service/src/autonomy-policy/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/autonomy-policy/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Clarify and extend autonomy boundaries.
- Technical value: Capability-based file/operation/cost policy without promising control over the entire App host.
- Product value: The user understands and controls permitted agent autonomy.
- Scope: `apps/local-service/src/autonomy-policy/service.mts`; `packages/contracts/autonomy/policy.ts`; `apps/local-service/src/runtime/sandbox-broker.mts`; `apps/web/src/features/autonomy/AutonomyManager.tsx`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: The user understands and controls permitted agent autonomy. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build document enforceable boundaries and impossible promises; reject narrow-path execution without enforcement. AC2: In the permitted route, exceeding scope/limit stops new dispatch; unknown outcome remains fenced. AC3: A monetary limit is allowed only with sufficient F11 metering/reservation; otherwise the UI clearly reports unavailability.
- Verification gates: `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: enforcement_capability_and_owner_design_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h design; build after enforcement confirmation; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + security-privacy-supply-chain-reviewer + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: enforcement_capability_and_owner_design_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

#### Completion report

- status: implemented
- what was done: Optional maxCommandsTotal adds a backward-compatible v1 policy-wide command reservation budget. Durable counting does not double-charge retries or refund unknown reservations, rejects new dispatch/runs/resume at the cap and allows the final admitted command to finish. UI separates reservations from observed counts; narrow paths and monetary/host-tool claims remain unsupported.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/llm/budgets-and-observability.en.md; docs/api/endpoints.en.md; docs/frontend/components.en.md; registry and scoped source checks.

### Task `PAOS-FUNC-16`

- Delivery group: `FUNC-G05`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-16 — Confirm available history and actually loaded profiles
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: none
- Source: host_history_not_exposed; loadedVersion/observedModel/observedEffort unknown. [apps/local-service/src/sessions/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/sessions/service.mts), [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Confirm available history and actually loaded profiles.
- Technical value: Separate configured/pinned/observed model, effort and asset version; capability-based history adapter.
- Product value: The user knows which agent actually ran and what history is available.
- Scope: `apps/local-service/src/sessions/service.mts`; `apps/local-service/src/team/service.mts`; `packages/contracts/team/assets.ts`; `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: The user knows which agent actually ran and what history is available. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build verify the supported host contract; inaccessible history is not retrieved by bypassing private stores. AC2: UI distinguishes configured/pinned/observed; loadedVersion appears only from a confirmed event. AC3: Reconnect/profile switch do not mix history and identity; explain partial coverage and missing attestation.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-run-navigation.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: supported_host_capability_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 6–12 h capability review; build after API confirmation; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: architect + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: supported_host_capability_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

#### Completion report

- status: implemented
- what was done: The official host contract was checked; paos_history_capability_v1 binds adapter/project/generation and separates available local history from host not_connected. Profile executionEvidence separates current configured and immutable run-pinned model/effort/version/hash; observed/loaded stay unavailable without attestation. Foreign profile cursors, project switches/late responses/restart were checked without private host scraping.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/agents/context.en.md; docs/ai/agents/sessions.en.md; docs/api/endpoints.en.md; docs/frontend/components.en.md; registry and scoped source checks.

### Task `PAOS-FUNC-17`

- Delivery group: `FUNC-G06`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-17 — Prepare usable installation, update and rollback
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Extension; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 08:40
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g06_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-22`
- Blocks: none
- Source: Portable CLI exists; signed installer/auto-update are not claimed. [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Prepare usable installation, update and rollback.
- Technical value: Define version/digest/signing, compatibility and recovery UX on top of the portable package.
- Product value: Updates do not require manual directory selection or endanger data.
- Scope: `apps/desktop-local/distribution.mts`; `apps/desktop-local/main.mts`; `apps/desktop-local/README.md`; `apps/launcher/launcher.ts`; `tests/web/desktop-local.test.mts`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Choosing a design without implementation and checks does not close this task.
- Expected result: Updates do not require manual directory selection or endanger data. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build choose distribution channel, installer format, signing and AUTH/licensing gates; publication is separate. AC2: Synthetic install/update/rollback preserve the profile; incompatible schema/tuple blocks startup with clear recovery. AC3: User profiles and older versions are not removed without a separate decision; a new clean Windows profile passes the agreed scenario.
- Verification gates: `node --test tests/web/desktop-local.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: distribution_signing_commercial_design_required; first bounded discovery/design, then concrete build scope and estimate; an unknown host capability is not treated as promised. Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: high — multiple contracts and a design gate
- Estimated execution time: 8–16 h design; build after distribution channel selection; rough_range_not_commitment. This estimates discovery/design; the total build estimate is not yet known.
- Agents: release-operator + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare and agree the design gate; do not start build before it.

#### Completion Report

- status: implemented
- what was done: Implemented managed setup/update/rollback/status/start over a private unsigned portable package with one home. Host tuple admission precedes writes; home→selection locks and source/target reservations preserve profile/version data. Environment whitelisting preserves the fresh service home and postcommit receipt loss is reported honestly. Actual relocated A/B/A CLI/NativeLauncher IPC/service/browser and incompatible-schema rollback were checked without checkout fallback.
- files touched / work locations: apps/desktop-local/distribution.mts; apps/desktop-local/main.mts; apps/desktop-local/README.md; apps/launcher/main.mts; tests/web/desktop-local-managed.test.mts; tests/web/single-window/managed-distribution-acceptance.mts; tests/web/single-window/managed-distribution.fixture.mts
- technical value delivered: Managed paths, exact tuple/selection admission, transfer leases, home→selection launch fencing and environment isolation are verified on actual relocated packages.
- product value delivered: One managed-home replaces manual version/profile directory selection; update/explicit rollback preserve data and expose refusal/recovery states.
- follow-up: No unfinished work in this card within G06; human/signing/public/commercial release and a new OS account remain separate gates.
- actual implementation date and time: 16-11-2026 08:40
- verification evidence: .tmp/func-g06/web-native-final.log:694/694,0fail/skip; .tmp/func-g06/managed-acceptance/evidence-mJ8j5k/result.json:10/10,cleanup=true; .tmp/func-g06/native-candidate.json:passed; .tmp/func-g06/native-default.json:passed; .tmp/func-g06/typecheck-final.log:passed; .tmp/func-g06/build-final.log:passed
- residual risks: Private unsigned user-space delivery on the existing Windows account; no new OS account/SID, actual native GUI/SmartScreen, system installation, signing/commercial/public release, provider/model or human acceptance. Cooperative managed profile reservations do not sandbox arbitrary SQLite writers. Every original file hash is preserved; explicitly recorded new empty WAL/32KiB SHM bookkeeping means whole-directory identity is not claimed. Rollback restores the explicitly selected compatible snapshot; newer work needs a fresh compatible backup.
- Documentation impact: updated; apps/desktop-local/README.md; docs/operations/install-start-stop.md; docs/operations/install-start-stop.en.md; docs/operations/release-boundaries.md; docs/operations/release-boundaries.en.md; docs/web/pilot.md; docs/web/pilot.en.md; docs/db/backup-restore.md; docs/db/backup-restore.en.md; registry RU/EN.

### Task `PAOS-FUNC-18`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-18 — Align task and dashboard snapshot refresh
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Improvement; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-07`, `PAOS-FUNC-26`, `PAOS-FUNC-27`
- Blocks: `PAOS-FUNC-19`
- Source: Task/dashboard use mainly initial/manual snapshots, queue polling is separate. [apps/web/src/features/tasks/TaskManager.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/TaskManager.tsx), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Align task and dashboard snapshot refresh.
- Technical value: Define refresh/invalidation contract for background work, mutations and project switches.
- Product value: After execution the user sees current status without guessing which screen to refresh.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/api/latest-request.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (new planned file); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/local-service/src/project-scans/service.mts` (new planned file). New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: After execution the user sees current status without guessing which screen to refresh. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: A task/queue change through another permitted channel either refreshes the screen or explicitly marks the snapshot stale. AC2: A late response from the previous project does not replace current data; refresh does not overwrite a dirty editor. AC3: Polling/subscription stop on unmount and do not create unbounded load. AC4: Create/modify/rename/delete and policy/root changes invalidate affected directory/document/graph/analysis snapshots; choose a watcher or bounded rescan/refresh with explicit freshness, without promising an unselected live watcher. AC5: Scan events include scanId/revision; late events from a cancelled job or another project do not change the UI. After return/restart show the retained scan status without overwriting drafts. AC6: The common freshness contract covers code/schema snapshots and code-table links: compatible revisions, late-response rejection, explicit stale and stopping polling on exit. F14/F33/F34 implement and test new consumers; F18 does not wait for them or block the early Files path.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: freshness_contract_before_build; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 6–12 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: No remaining work in this task; future consumers/packaging/performance retain their own tasks.

#### Completion Report

- status: implemented
- what was done: Atomic task snapshot/profile stamp, bounded single-flight polling, explicit stale/refresh in Dashboard/Task Manager/overlay and dirty CAS conflicts are implemented; explicit file refresh and shared provenance invalidation do not claim a live watcher. Scan attempt/request scopes reject late events.
- files touched / work locations: packages/contracts/project-freshness.ts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/api/project-freshness.ts; apps/web/src/ui/ProjectFreshness.tsx; apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/dashboard/Dashboard.tsx; tests/web/project-freshness.test.mts; tests/web/project-freshness-poll.test.mts
- technical value delivered: Shared root/policy/revision contracts and final authority fences verified on current API/SQLite/FS/build/native fixtures.
- product value delivered: Partial and stale observations are explicit; execution limits are explained before dispatch while source data and drafts are preserved.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: No remaining work in this task; future consumers/packaging/performance retain their own tasks.
- Documentation impact: updated; docs/frontend/state-management.md; docs/frontend/state-management.en.md; docs/api/events.md; docs/api/events.en.md; docs/backend/recovery.md; docs/backend/recovery.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-19`

- Delivery group: `FUNC-G07`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-19 — Check end-to-end functionality on the current build
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Verification; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; inclusion in the plan does not start implementation.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-02`, `PAOS-FUNC-03`, `PAOS-FUNC-04`, `PAOS-FUNC-05`, `PAOS-FUNC-06`, `PAOS-FUNC-07`, `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-24`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-14`, `PAOS-FUNC-33`, `PAOS-FUNC-34`
- Blocks: `PAOS-FUNC-23`
- Source: Redesign visual/synthetic receipts do not prove the new native full path. [design/2026-11-13-v3/implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md), [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Check end-to-end functionality on the current build.
- Technical value: Link real UI/API/storage/native receipts to one revision without substituting mock execution data.
- Product value: The user completes the entire working journey and receives a verifiable result.
- Scope: `tests/web/single-window/m4-integration-acceptance.mts`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`; `tests/web/single-window/m2b-browser-acceptance.mts`; `tests/web/single-window/m2c-browser-acceptance.mts`; `tests/web/single-window/project-files-browser-acceptance.mts` (new planned file); `tests/web/project-files.test.mts` (new planned file); `tests/web/project-scans.test.mts` (new planned file); `tests/web/project-analysis.test.mts` (new planned file). New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The user completes the entire working journey and receives a verifiable result. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: The synthetic task→assignment→run→approval→command→diff/checks→owner acceptance path passes on the current build. AC2: Forms, custom workflow, RU/EN, both themes, keyboard, links and partial/error states are checked after F02–F07/F10/F18. AC3: Actual App/model roundtrip and agent/skill generation are tested only with separate authorization; without it record the live gap, which a synthetic pass does not close. AC4: On a synthetic fixture test Add → immediately available tree → scan stages → allowed file preview → task file reference; map and discovery do not substitute for complete file-tree coverage. AC5: Test empty/no-Control-plane/Python-only/mixed projects, Unicode/spaces, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift during scan, cancel/restart/retry and two projects. An individual file failure preserves the allowed portion, root violations are blocked; before/after target hashes match. AC6: Verify RU/EN, two themes, keyboard/focus, pagination, explicit incomplete search and absence of false-ready; fixtures use no real profiles/credentials and execute no target scripts. AC7: After F14/F33/F34 test the expanded Files → Map → DB schema → code usages → source line → task reference journey; preserve selection/back/filter/project isolation. Verify confirmed/inferred/unresolved, runtime schema vs ORM/migrations, Mermaid export and bounded large graphs. AC8: New tabs/sections have RU/EN, both themes, keyboard/focus, accessible list/table fallback and all UI states; backend failure/cancel/restart are not masked by mock UI. Separate early Files/scan receipts are allowed before graph/DB, but final F19 closure requires the expanded scenario.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1`; `npm run build:web` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: separate_synthetic_and_actual_runtime_receipts; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 8–16 h without waiting for live approval; rough_range_not_commitment. Refine on the current build before starting.
- Agents: tester + reviewer; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Check dependencies and whether the finding remains current. Prepare a reproducible scenario and record the initial state.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: separate_synthetic_and_actual_runtime_receipts; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

### Task `PAOS-FUNC-20`

- Delivery group: `FUNC-G04`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-20 — Measure scaling and long-running behavior
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Verification; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Blocks: `PAOS-FUNC-09`
- Source: Large projects/long-running behavior after redesign have not been measured; runtime index/cache caps. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Measure scaling and long-running behavior.
- Technical value: Reproducible workload with hardware/cache profile, latency/RSS/queue-depth and error budgets.
- Product value: Large projects and long sessions remain manageable.
- Scope: `tests/web/storage.test.mts`; `tests/web/code-index.test.mts`; `tests/web/ui-stream-search.test.mts`; `tests/web/single-window/functional-scale-acceptance.mts` (new planned file); `research/product-agent-os-web-prd-2026-11-05.md`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/project-inventory/service.mts` (new planned file); `apps/local-service/src/project-scans/service.mts` (new planned file); `apps/local-service/src/project-analysis/service.mts` (new planned file). New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Large projects and long sessions remain manageable. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Record hardware/cache and volumes: 10k tasks, 100k messages, 1k files; separately check boundaries of 1001 files and 9 projects. AC2: Measure cold startup, search/list/event-visible latency, RSS and snapshots in a repeatable long run; no hidden data loss. AC3: Compare results against WEB-NFR and agreed thresholds; record deviations under F09 and explicitly limit unsupported volumes. AC4: Fix budgets and dataset before measurement: large monorepo, wide/deep directory, empty folders, generated/vendor/ignored, binary/large, mixed languages. Measure registration-to-tree, expansion/search, scan phases, cancellation latency, restart recovery, RSS, traversal count and bytes read. AC5: Test legacy limits 1000/1001 files, 10000/10001 entries, depth 32/33, 512KiB and 8MiB as correct partial/bounded outcomes, not a demand to remove guards. Metadata listing need not read all project contents. AC6: Baseline can precede F26–F29; final F20 closure requires their version and comparison with baseline. F09 uses this protocol for before/after; the benchmark does not modify the user workspace. AC7: One reproducible benchmark protocol sets ground truth and budgets for F30/F31/F32: cold/incremental scan, RSS/disk, latency and precision/recall. F14/F33/F34 add UI responsiveness, schema size, edge limits and bounded agent-context cost; they repeat the protocol in their own AC. F20 does not depend on completion of PoC/DB/graph, avoiding an F20→F09→F14 cycle.
- Verification gates: `npm run test:web-m1` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: benchmark_protocol_and_thresholds_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 8–16 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: tester + architect; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.

#### Completion Report

- status: implemented
- what was done: Pinned protocol/hardware/cache/ground truth before measurement; retained baseline failure and repeated after/final on10k tasks/100k messages/1000 documents/1000 code files with120ssoak and exact boundaries. Outcome is measured_with_deviations/bounded_outcomes, not all-NFR pass.
- files touched / work locations: tests/fixtures/func_g04/protocol.json; tests/web/single-window/functional-scale-acceptance.mts; tests/web/single-window/graph-database-browser-acceptance.mts
- technical value delivered: Reproducible source-bound measurements, SQL integrity, bytes/walks/RSS and actual application scan/recovery replace assumptions.
- product value delivered: Supported flows, waiting time and scale limits are explicit without hidden data loss.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; Current closure diagnostic/reference/filesystem: .tmp/func-g04/scale-closure/result-diagnostic-1794778219987.json; .tmp/func-g04/scale-closure/result-reference-1794778236139.json; .tmp/func-g04/scale-closure/result-filesystem-1794778628384.json; 133 current source hashes; SQL 10k/100k/1k integrity/FK0; soak 120.15 s / 119 iterations; preserved targets + cleanup; unchanged protocol 37c20aadc0d3474ef78cf86928e9ee1727be7bf415152fc393e92c8b079af625
- residual risks: Cold history/catalog generations exceed the 1000 ms comparison in retained runs; exact samples/deviations are in the F20 receipts. 10k/10001 directories yield a bounded 30 s timeout. Reference 4-core/GUI cold launch/whole-system RSS are not qualified. Browser sampled aggregate 1101.32 MiB is diagnostic, not a per-process peak. Human/provider/release remain separate.
- follow-up: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.
- Documentation impact: updated; docs/testing/test-map.md; docs/testing/test-map.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-21`

- Delivery group: `FUNC-G06`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-21 — Recheck queue, Stop and crash recovery
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Verification; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 08:11
- Priority: P1
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g06_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-23`
- Source: Recovery/ownership implemented; current-run regression is required. [apps/local-service/src/recovery/recipe-checkpoint.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/recovery/recipe-checkpoint.mts), [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Recheck queue, Stop and crash recovery.
- Technical value: Check identity/CAS/lease/ownership fences and absence of replay in failures.
- Product value: Connection loss neither starts a task twice nor loses the result.
- Scope: `tests/web/recipe-recovery.test.mts`; `tests/web/recipe-crash.test.mts`; `tests/web/scheduler-runtime.test.mts`; `tests/web/parallel-workspaces.test.mts`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Connection loss neither starts a task twice nor loses the result. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Cover crash before dispatch, after dispatch before receipt, and after terminal receipt as separate scenarios. AC2: Stop without ACK does not release ownership; lost consumer/timeout require proper reconciliation. AC3: Allowed parallelism remains across different roots, overlapping roots are blocked; selective Stop does not cancel another run.
- Verification gates: `node --test tests/web/recipe-recovery.test.mts tests/web/recipe-crash.test.mts tests/web/scheduler-runtime.test.mts tests/web/parallel-workspaces.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: disposable_profiles_only; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 8–16 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: tester + reviewer; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare a reproducible scenario and record the initial state.

#### Completion Report

- status: implemented
- what was done: Three actual-process SIGKILL boundaries (before dispatch, in-flight without receipt, terminal receipt) were checked with DB reopen. Run identity/ownership, explicit resume and successor-only dispatch are preserved; unknown/cancel without ACK does not release scope. Root overlap/parallel/selective Stop checks pass.
- files touched / work locations: tests/web/recipe-crash.test.mts; tests/web/recipe-crash.fixture.mts
- technical value delivered: Actual process crash boundaries verify durable identity, explicit resume, Stop ownership and absence of replay.
- product value delivered: Crash/reconnect does not create a duplicate run; unknown outcomes and missing Stop ACK remain explicit recovery states.
- follow-up: No unfinished work in this card within G06; human/signing/public/commercial release and a new OS account remain separate gates.
- actual implementation date and time: 16-11-2026 08:11
- verification evidence: .tmp/func-g06/f21-focused-final.log:20/20,0fail/skip; .tmp/func-g06/web-native-final.log:694/694,0fail/skip; .tmp/func-g06/managed-acceptance/evidence-mJ8j5k/result.json:10/10,cleanup=true; .tmp/func-g06/native-candidate.json:passed; .tmp/func-g06/native-default.json:passed; .tmp/func-g06/typecheck-final.log:passed; .tmp/func-g06/build-final.log:passed
- residual risks: Private unsigned user-space delivery on the existing Windows account; no new OS account/SID, actual native GUI/SmartScreen, system installation, signing/commercial/public release, provider/model or human acceptance. Cooperative managed profile reservations do not sandbox arbitrary SQLite writers. Every original file hash is preserved; explicitly recorded new empty WAL/32KiB SHM bookkeeping means whole-directory identity is not claimed. Rollback restores the explicitly selected compatible snapshot; newer work needs a fresh compatible backup.
- Documentation impact: updated; docs/backend/recovery.md; docs/backend/recovery.en.md; source registry RU/EN.

### Task `PAOS-FUNC-22`

- Delivery group: `FUNC-G06`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-22 — Recheck import, backup and restore
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Verification; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 08:11
- Priority: P1
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g06_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-17`, `PAOS-FUNC-23`
- Source: Import/backup contracts exist; current combined verification is absent. [apps/local-service/src/import-export/migration.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/import-export/migration.mts), [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Recheck import, backup and restore.
- Technical value: Check source authority, freeze/CAS, counts/hashes/FK, blobs and idempotency.
- Product value: Tasks, history and attachments survive migration and recovery.
- Scope: `tests/web/domain-migration.test.mts`; `tests/web/storage-backup.test.mts`; `apps/local-service/src/import-export/migration.mts`. Ownership is assigned at start; listed roles are proposals, agents are not running now.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: Tasks, history and attachments survive migration and recovery. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Source drift and unknown writer stop cutover; two writable authorities never arise. AC2: Corrupt/missing blob, interrupted import and request replay yield safe results without duplicates. AC3: Restore into a new synthetic profile preserves data and links; old profile is unchanged; credentials/pending operations are not replayed.
- Verification gates: `node --test tests/web/domain-migration.test.mts tests/web/storage-backup.test.mts` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: synthetic_data_no_real_profile_mutation; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 6–12 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: tester + reviewer; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Next step: Check dependencies and whether the finding remains current. Prepare a reproducible scenario and record the initial state.

#### Completion Report

- status: implemented
- what was done: Checked source drift/unknown-writer freeze/CAS, interrupted pre-promotion retry without duplicate tasks, committed-receipt replay, corrupt/missing blobs, independent FK validation despite self-consistent hashes, new-profile restore and stale approvals/pending outbox/cursors. Source authority/profile/source bytes are preserved.
- files touched / work locations: tests/web/domain-migration.test.mts; tests/web/storage-backup.test.mts
- technical value delivered: Freeze/CAS, interrupted-promotion retry and independent integrity/FK/blob checks are verified by current native synthetic checks.
- product value delivered: Tasks, history, settings and attachments survive transfer/restore; original data is not overwritten.
- follow-up: No unfinished work in this card within G06; human/signing/public/commercial release and a new OS account remain separate gates.
- actual implementation date and time: 16-11-2026 08:11
- verification evidence: .tmp/func-g06/f22-focused.log:11/11,0fail/skip; .tmp/func-g06/web-native-final.log:694/694,0fail/skip; .tmp/func-g06/managed-acceptance/evidence-mJ8j5k/result.json:10/10,cleanup=true; .tmp/func-g06/native-candidate.json:passed; .tmp/func-g06/native-default.json:passed; .tmp/func-g06/typecheck-final.log:passed; .tmp/func-g06/build-final.log:passed
- residual risks: Private unsigned user-space delivery on the existing Windows account; no new OS account/SID, actual native GUI/SmartScreen, system installation, signing/commercial/public release, provider/model or human acceptance. Cooperative managed profile reservations do not sandbox arbitrary SQLite writers. Every original file hash is preserved; explicitly recorded new empty WAL/32KiB SHM bookkeeping means whole-directory identity is not claimed. Rollback restores the explicitly selected compatible snapshot; newer work needs a fresh compatible backup.
- Documentation impact: updated; docs/db/backup-restore.md; docs/db/backup-restore.en.md; source registry RU/EN.

### Task `PAOS-FUNC-23`

- Delivery group: `FUNC-G07`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-23 — Conduct product acceptance of key scenarios
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Verification; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: verification_gap
- Execution authority: planning_only; inclusion in the plan does not start implementation.
- Depends on: `PAOS-FUNC-19`, `PAOS-FUNC-21`, `PAOS-FUNC-22`, `PAOS-FUNC-24`
- Blocks: none
- Source: PRD pilot metrics and UI-12 acceptance remain separate gates. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [docs/planning/2026-11-13-v3-ui-implementation-plan.md](2026-11-13-v3-ui-implementation-plan.md). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Conduct product acceptance of key scenarios.
- Technical value: Tie acceptance to observable correctness of decisions, not number of clicks.
- Product value: The user understands status, blocker, evidence and next action without prompting.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The user understands status, blocker, evidence and next action without prompting. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before the pilot agree participants, scenarios, opt-in/retention and MD/chat baseline; production data is not required. AC2: Cover first opening, return, conflict, partial evidence and acceptance; document comprehension errors alongside successes. AC3: Test PRD goals of 4/5 in 3 minutes and 3/5 reuse in 14 days as hypotheses; zero false interpretations of verified and data loss; owner accepts results separately. AC4: Add folder selection, finding an ordinary file outside Control-plane, explaining excluded/unsupported/partial, cancel/retry and return after restart. Observer checks that the participant does not confuse file visibility, successful indexing and execution authorization. AC5: Human pilot includes finding a change location via Map and DB usages, reading ERD/table, navigating to source, understanding stale/partial/inferred and discovering unsupported semantics. Compare success and time with the agreed baseline; UI convenience is not inferred from technical tests.
- Verification gates: Observed pilot under agreed protocol; there is no automated equivalent of human acceptance. These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: human_pilot_protocol_and_consent_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 6–12 h preparation/analysis plus 14 days of observation, not a development duration; rough_range_not_commitment. Refine on the current build before starting.
- Agents: product-manager + tester; human acceptance — owner; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Check dependencies and whether the finding remains current. Prepare a reproducible scenario and record the initial state.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: human_pilot_protocol_and_consent_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

### Task `PAOS-FUNC-24`

- Delivery group: `FUNC-G07`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-24 — Explain capability availability at the point of action
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Improvement; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; inclusion in the plan does not start implementation.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-10`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-14`, `PAOS-FUNC-33`, `PAOS-FUNC-34`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-23`
- Source: Several screens already show unknown/staged; a unified journey check is needed. [apps/web/src/ui/ConnectionControls.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/ConnectionControls.tsx), [apps/web/src/features/artifacts/ArtifactExplorer.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/artifacts/ArtifactExplorer.tsx). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Explain capability availability at the point of action.
- Technical value: Unified capability vocabulary for staged/unsupported/partial/connected/qualified/accepted.
- Product value: The user distinguishes an available capability from a screen offering a future one.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/ui/ConnectionControls.tsx`; `apps/web/src/locales/app.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (new planned file); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (new planned file); `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The user distinguishes an available capability from a screen offering a future one. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: For usage, graph, proposals, skills discovery, history, autonomy and runtime, show actual scope and reason for unavailability next to the action. AC2: Provide a concrete next step; unsupported does not look like loading, connected is not called execution-qualified. AC3: RU/EN and accessibility states are checked; no repeated request for already valid bounded authority. AC4: Onboarding and project show independent registration/tree/inventory/documents/code/analysis states from F26–F29, observation time and scope; counts.files is not called indexed without corresponding coverage. AC5: Empty/no-supported-code does not get a false “project fully analyzed”; excluded/error/unsupported explain reason and action. An unavailable parser/core adapter does not hide the available tree; the Control-plane checklist is explicitly named as a separate filter. AC6: Project navigation and onboarding clearly distinguish Files, Map, DB schema and code usages; Settings owns registration/source and does not duplicate standalone explorers. F14/F33/F34 deliver production UI; early capability states are available before their completion, but full F24 closure requires all consumers. AC7: UI shows only implemented capabilities/languages/DB sources and explains absence: not_configured, unsupported, unavailable, indexing, partial, stale, failed. PoC/experimental is not called production-ready; the product selects an engine on evidence, and internal backend settings are not imposed on the user.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: capability_wording_review_required; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 8–16 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: product-manager + builder + tester; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Check dependencies and whether the finding remains current. Assign an owner and refine the smallest verifiable slice.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: capability_wording_review_required; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.

### Task `PAOS-FUNC-25`

- Delivery group: `FUNC-G07`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-25 — Align current product statuses and criteria
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Documentation; functional audit after V3 redesign and owner request for a task matrix.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; inclusion in the plan does not start implementation.
- Depends on: none
- Blocks: none
- Source: Dated addenda coexist with early status blocks; a current-state entry is needed. Current docs unittest: 4 failures due to missing rendered accessibility/pilot RU/EN and search/sitemap parity. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [PLAN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/PLAN.md). Provenance: 15.11.2026 static audit; no new runtime results are claimed.
- Short description: Align current product statuses and criteria.
- Technical value: One current PRD/architecture/plan/registry pointer with history preserved.
- Product value: The plan and documentation clearly show what works, what is limited, and what awaits verification.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/web/accessibility.md`; `docs/web/accessibility.en.md`; `docs/web/pilot.md`; `docs/web/pilot.en.md`. New paths are marked planned; a file introduced by another task is used only after that task.
- Non-goals: changes outside the specified behavior; publication, real credentials, provider calls and hook/trust changes. Other people’s dirty changes are outside the fix.
- Expected result: The plan and documentation clearly show what works, what is limited, and what awaits verification. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Current scope/status/acceptance do not conflict with historical implementation_not_started/API-only blocks: history is explicitly marked and routed. AC2: F01–F34 and M5 have a single owner/status/source; implemented does not substitute for human/live acceptance. AC3: Synchronize only changed claims and RU/EN registry; validators/docs tests pass, old 56 cards are preserved. AC4: Current docs-site checks no longer report missing web/accessibility.html and web/pilot.html in RU/EN; search/sitemap/switcher parity is confirmed on an explicitly selected build. Site publication and promotion are separate. AC5: Docs distinguish Sources, F26 file tree, F27 scanning, F28 inventory policy and F29 discovery; API/coverage versions, recovery and limitations are documented in existing PRD/architecture without claiming automatic repair or full semantics. AC6: F30–F34 contain upstream URLs, research date, selected version/commit/license and actual PoC receipts when executed; README claims are not presented as local measurements. PRD/architecture/UI help describe Map/Database/usages tabs, read-only sources, export, coverage and fallback; links and RU/EN are aligned.
- Verification gates: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`; `python tools/check_docs.py`; `git diff --check` These are future task checks, not checks performed by this planning. Check positive, failure and recovery scenarios in the specified scope. General docs gates apply when documentation changes.
- Risks / approval gates: source_reconciliation_not_history_deletion; Real profiles, external service, publication and provider/model calls require separate exact authorization. Synthetic acceptance uses disposable roots only.
- Complexity: medium — bounded scenario with negative checks
- Estimated execution time: 4–8 h; rough_range_not_commitment. Refine on the current build before starting.
- Agents: docs-maintainer + product-manager; assign independent areas before execution; exclude concurrent writes to one file.
- Skills: implementation-planner for planning; task-matching implementation/verification skills are chosen at start, without installing new skills for this task.
- Output artifacts: scoped diff in listed work locations; check results and Documentation impact in this Completion Report; status in this group’s JSON; short handoff in RUNLOG.md.
- Rollback: undo only own hunks after checking drift; for data use retained synthetic backup and agreed recovery contract; destructive Git is not allowed.
- Planning update 15.11.2026: acceptance and links to F26–F29 expanded; execution has not started.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Verify that the finding remains current. Assign an owner and refine the smallest verifiable slice.

#### Completion Report

- status: planned
- what was done: task formulated in the plan; implementation and its acceptance scenarios have not started.
- files touched / work locations: implementation none; planned work locations are listed in Scope.
- technical value delivered: implementation result not yet obtained.
- product value delivered: user outcome not yet confirmed.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: only original links and static observations in Source; future Verification gates were not executed by this task.
- residual risks: source_reconciliation_not_history_deletion; current source state is rechecked at start.
- follow-up: Next step above; after execution synchronize JSON status, this card and only affected control-plane claims.
- Documentation impact: planning_only; code and functional claims do not change yet. On completion reconcile changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required and evidence in this report.


### Task `PAOS-FUNC-26`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-26 — Add a project file browser
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request for project file directory and managed scanning; multi-stage functional scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`, `PAOS-FUNC-33`
- Source: Sources shows six fixed Control-plane files; catalog reads .md/.txt, graph selected sources. Checked onboarding has no unified tree or independent directory API. [apps/local-service/src/adapters/project-sources.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts), [apps/web/src/ui/Operations.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/Operations.tsx), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/web/src/features/graph/GraphExplorer.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/graph/GraphExplorer.tsx). Sources were read in the 15.11.2026 analysis; runtime was not run.
- Short description: Add a project file browser.
- Technical value: Graph-independent directory and safe-reader API with lazy loading, stable links and bounded responses.
- Product value: The user sees the selected folder structure and opens accessible files even when the index is not ready or the language is unsupported.
- Scope: `packages/contracts/project-files.ts` (new planned file); `apps/local-service/src/project-files/service.mts` (new planned file); `apps/local-service/src/http/application.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (new planned file); `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/locales/app.ts`; `tests/web/project-files.test.mts` (new planned file); `tests/web/single-window/project-files-browser-acceptance.mts` (new planned file). New paths are marked planned; a file introduced by another task is used only after that task.
- Architecture boundary: project-files API → checked filesystem metadata/read → ProjectFiles UI; graph readiness is not a precondition.
- Non-goals: Editing, deleting and moving files; terminal; executing preview code; automatic transfer of content to a model.
- Expected result: The user sees the selected folder structure and opens accessible files even when the index is not ready or the language is unsupported. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: After registration the Files section is available without a graph or completed scan; nested and empty directories, source files, configurations and binary files as metadata are visible within allowed F28 policy. AC2: Expanding a directory loads only the needed branch; pagination and filters show selection bounds; filename/path search explicitly states scope. Metadata includes relativePath, type, size, modifiedAt and access state. AC3: Text is read by a separate request with root identity, revision, size and encoding checks; binary/oversized/unreadable receive explanations. Extensions unsupported by the indexer do not hide files. HTML/scripts are not executed during preview. AC4: No root escape through traversal, symlink/junction/hardlink or directory substitution; sensitive content is not exposed. Selecting a file does not send the whole project to a model or grant execution authority. AC5: The selected path can be copied and used as a file reference; Control-plane is a filter over actual paths. Project switches and late responses do not mix trees; RU/EN, keyboard, focus, empty/error/loading are tested. AC6: File/line navigation supports future transitions from Map/Database/code usages and return to the selected file; inaccessible/deleted source is explained. F26 does not wait for F30–F34; an absent capability's backend action does not display a false result.
- Verification gates: `node --test tests/web/project-files.test.mts tests/web/project-inventory.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`; `npm run build:web`. Expect exit0 and all scoped AC passing on synthetic fixtures. These commands are future work: new tests/harness do not exist yet. Browser acceptance uses an agreed runner protocol and disposable roots; exact flags are fixed before build. If core Python modules change, also run focused tests and the full TEST.md plugin/runtime route. Recheck runtime tuple before native acceptance after pinned sources change.
- Risks / approval gates: directory_api_ui_contract_review_required; status=proposal_staged, design gate owner — builder + tester; product-manager accepts the viewing scenario. Before build approve API/policy/state contract, source ownership and recovery. No provider/live calls, dependency installation or existing-profile changes without separate exact authorization.
- Complexity: high — API, filesystem boundary and handling incomplete results.
- Estimated execution time: 24–40 h, rough planning range; refine after API/UI contract; not a schedule commitment.
- Agents: builder + tester; product-manager accepts the viewing scenario; roles are proposed, subagents are not running. Change shared API/storage/UI files sequentially with owners of dependent tasks.
- Skills: implementation-planner for this planning; choose task-matching runtime/frontend/test skills at start. For Python implementation follow existing python-design-patterns/python-code-style guidance.
- Output artifacts: Verifiable tree and read-only reader, typed API, focused/browser receipts in this card. Status is this group's JSON; evidence and Documentation impact are in this Completion Report; compact handoff is RUNLOG.md.
- Rollback: only own changes after checking drift; test schema/recovery changes on a disposable profile. Do not change target files; retain the old successful snapshot until atomic publication of the new one.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Complete F29/F10/F18 and final FUNC-G03 gates.

#### Completion Report

- status: implemented
- what was done: Implemented lazy project Files, bounded directory search/paging, checked reader, source/metadata pins, copy and deep links in RU/EN and both themes.
- files touched / work locations: apps/local-service/src/project-files/service.mts; apps/web/src/features/files/ProjectFiles.tsx; apps/local-service/src/http/application.mts; apps/web/src/ui/App.tsx; tests/web/project-files-api.test.mts
- technical value delivered: Registry/root/policy/revision contracts verified through actual HTTP/SQLite/FS and production React.
- product value delivered: Project sources are available with explicit unavailable reasons and preserved navigation.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Complete F29/F10/F18 and final FUNC-G03 gates.
- Documentation impact: updated; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-27`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-27 — Make scanning a managed background job
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request for project file directory and managed scanning; multi-stage functional scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-14`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`, `PAOS-FUNC-29`, `PAOS-FUNC-33`
- Source: POST /projects commits registration then awaits inspectProjectSources/codeIndex.rebuild. Scan summary is not a durable job; once receipts are in memory and expire after 10 minutes. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts), [apps/web/src/features/projects/ProjectOnboarding.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/projects/ProjectOnboarding.tsx), [tests/web/settings-desktop.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/web/settings-desktop.test.mts). Sources were read in the 15.11.2026 analysis; runtime was not run.
- Short description: Make scanning a managed background job.
- Technical value: Persisted scan IDs and stages, bounded worker, idempotency, cancel, retry and recovery separate from project registration.
- Product value: The project is available immediately after registration; the user sees progress, partial results and how to continue after failure.
- Scope: `packages/contracts/project-scan.ts` (new planned file); `apps/local-service/src/project-scans/service.mts` (new planned file); `apps/local-service/src/http/application.mts`; `apps/local-service/src/storage/local-store.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/storage/migrations/schema.mts`; `apps/local-service/src/code-index/service.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/projects/ProjectOnboarding.tsx`; `tests/web/project-scans.test.mts` (new planned file); `tests/web/settings-desktop.test.mts`. New paths are marked planned; a file introduced by another task is used only after that task.
- Architecture boundary: project registration → profile-owned scan job → bounded analyzers; independent lifecycle and source authority.
- Non-goals: Starting tasks/agents, provider calls, automatic execution of project commands and changing target files; an endless watchdog.
- Expected result: The project is available immediately after registration; the user sees progress, partial results and how to continue after failure. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Registration is saved once and returns an accessible project without waiting for full traversal; scan status includes scanId, root identity, policy version, inventory/documents/code/analysis stage, start/update times, counters and partial/error reasons. AC2: Repeated Add/retry including after restart does not create another project or duplicate work; concurrent requests for one revision merge or receive an explainable conflict. A changed root does not continue the old job. AC3: Cancel stops further work and late publication; retry starts with an explicitly defined revision. Restart recovers or moves the job to recovery_required/interrupted; unfinished work does not become completed. AC4: Define time/memory/entry and concurrency budgets; failure of one analyzer preserves allowed results of other stages. Readiness of one index does not mean complete project analysis; an unconnected analysis adapter displays unavailable. AC5: State and last successful coverage remain available after opening Settings/project and restart; events or bounded polling do not overwrite a newer revision. Scan bookkeeping stays in the PAOS profile; target workspace is not changed. AC6: A versioned analyzer contract permits code/schema/code_database stages with separate capabilities/status/progress, cancellation and atomic publication. F30–F32 evaluate external executors in isolation; F14/F33/F34 connect only selected ones; F27 does not depend on their implementation or automatically run installers.
- Verification gates: `node --test tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts tests/web/code-index.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Expect exit0 and all scoped AC passing on synthetic fixtures. These commands are future work: new tests/harness do not exist yet. Browser acceptance uses an agreed runner protocol and disposable roots; exact flags are fixed before build. If core Python modules change, also run focused tests and the full TEST.md plugin/runtime route. Recheck runtime tuple before native acceptance after pinned sources change.
- Risks / approval gates: persisted_scan_state_recovery_schema_design_required; status=proposal_staged, design gate owner — architect + builder + tester. Before build approve API/policy/state contract, source ownership and recovery. No provider/live calls, dependency installation or existing-profile changes without separate exact authorization.
- Complexity: high — API, filesystem boundary and handling incomplete results.
- Estimated execution time: 24–40 h, rough planning range; storage/recovery design before build; not a schedule commitment.
- Agents: architect + builder + tester; roles are proposed, subagents are not running. Change shared API/storage/UI files sequentially with owners of dependent tasks.
- Skills: implementation-planner for this planning; choose task-matching runtime/frontend/test skills at start. For Python implementation follow existing python-design-patterns/python-code-style guidance.
- Output artifacts: Durable scan lifecycle and progress UI; schema compatibility/rollback and crash/cancel/retry receipts. Status is this group's JSON; evidence and Documentation impact are in this Completion Report; compact handoff is RUNLOG.md.
- Rollback: only own changes after checking drift; test schema/recovery changes on a disposable profile. Do not change target files; retain the old successful snapshot until atomic publication of the new one.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: Complete F29/F10/F18 and final FUNC-G03 gates.

#### Completion Report

- status: implemented
- what was done: Idempotent registration returns queued before traversal; profile-owned CAS persists stages/progress/restart/retry/cancel, publication guards retain the previous graph. Persisted status UI is mounted.
- files touched / work locations: apps/local-service/src/project-scans/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/http/application.mts; apps/web/src/features/projects/ProjectScanStatus.tsx; tests/web/project-scans-api.test.mts
- technical value delivered: Registry/root/policy/revision contracts verified through actual HTTP/SQLite/FS and production React.
- product value delivered: Project sources are available with explicit unavailable reasons and preserved navigation.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Complete F29/F10/F18 and final FUNC-G03 gates.
- Documentation impact: updated; docs/backend/lifecycle.md; docs/backend/lifecycle.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-28`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-28 — Unify inventory, coverage and exclusions
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request for project file directory and managed scanning; multi-stage functional scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 20:10
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-02`, `PAOS-FUNC-10`, `PAOS-FUNC-14`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-33`
- Source: scanCheckedSources uses a hard denylist and extension filter, does not return all skips or read .gitignore; a limit on eligible files can interrupt traversal. Metadata, read and indexing coverage require separate contracts. [apps/local-service/src/code-index/sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/sources.mts), [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/local-service/src/adapters/project-sources.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts). Sources were read in the 15.11.2026 analysis; runtime was not run.
- Short description: Unify inventory, coverage and exclusions.
- Technical value: Shared path, revision and coverage contract for directory/document/code consumers with separate listing, reading and indexing rights.
- Product value: Files do not disappear from the overview because a language analyzer is missing; users understand what was found, skipped or inaccessible.
- Scope: `packages/contracts/project-inventory.ts` (new planned file); `apps/local-service/src/project-inventory/service.mts` (new planned file); `apps/local-service/src/code-index/sources.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/adapters/project-sources.ts`; `tests/web/project-inventory.test.mts` (new planned file); `tests/web/code-index.test.mts`; `tests/web/skill-generation-artifacts.test.mts`. New paths are marked planned; a file introduced by another task is used only after that task.
- Architecture boundary: checked filesystem inventory → per-consumer visibility/read/index policy; source root remains the file owner.
- Non-goals: Unconditional removal of existing limits or denylist; full traversal of excluded directories; secrets in indexes; a new independent scanner without assessing reuse.
- Expected result: Files do not disappear from the overview because a language analyzer is missing; users understand what was found, skipped or inaccessible. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: The contract distinguishes discovered, readable, indexed, unsupported, excluded and error; counters define different stages and do not sum overlapping sets as total files. Empty and unknown differ; no suitable code does not imply complete analysis. AC2: The file tree is independent of indexer extensions. .gitignore and project include/exclude have explicit precedence and separate visibility/indexing rules; ignore grants no access. Sensitive paths/content remain protected even with include override. AC3: Report applied policy version, skip reasons, limits and partial coverage. Heavy generated/vendor directories are not read unnecessarily; allowed metadata disclosure does not remove content-reading restrictions. AC4: Individual file error, size overrun or unsupported encoding preserves other permitted entries; directory-level denial marks incompleteness. Root identity drift, root escape attempt or unreliable revision blocks publication of unsafe results. AC5: Bounded/paged inventory supports normalized relative paths, Unicode/spaces and Windows case semantics; links and race conditions do not expand root. Identical policy/root/revision yield consistent references and reasons across consumers. AC6: Policy changes invalidate affected snapshots; file metadata does not require reading all sources. Positive/negative scenarios and load boundaries are tested; project sources remain unchanged. AC7: PoCs and future adapters apply the same root/policy/read/index rules and show coverage mismatches; third-party indexers do not bypass exclusions or create caches in the target. Discovered DB/ORM/migration candidates are metadata, not permission to connect or run migrations; scan limits and sensitive paths remain protected.
- Verification gates: `node --test tests/web/project-inventory.test.mts tests/web/code-index.test.mts tests/web/skill-generation-artifacts.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`. Expect exit0 and all scoped AC passing on synthetic fixtures. These commands are future work: new tests/harness do not exist yet. Browser acceptance uses an agreed runner protocol and disposable roots; exact flags are fixed before build. If core Python modules change, also run focused tests and the full TEST.md plugin/runtime route. Recheck runtime tuple before native acceptance after pinned sources change.
- Risks / approval gates: inventory_policy_security_boundary_design_required; status=proposal_staged, design gate owner — architect + builder + security-privacy-supply-chain-reviewer + tester. Before build approve API/policy/state contract, source ownership and recovery. No provider/live calls, dependency installation or existing-profile changes without separate exact authorization.
- Complexity: high — API, filesystem boundary and handling incomplete results.
- Estimated execution time: 12–20 h, rough planning range; choose reuse/adapter before build; not a schedule commitment.
- Agents: architect + builder + security-privacy-supply-chain-reviewer + tester; roles are proposed, subagents are not running. Change shared API/storage/UI files sequentially with owners of dependent tasks.
- Skills: implementation-planner for this planning; choose task-matching runtime/frontend/test skills at start. For Python implementation follow existing python-design-patterns/python-code-style guidance.
- Output artifacts: Shared inventory/coverage contract and consumer migration without weakening guards; fixture evidence. Status is this group's JSON; evidence and Documentation impact are in this Completion Report; compact handoff is RUNLOG.md.
- Rollback: only own changes after checking drift; test schema/recovery changes on a disposable profile. Do not change target files; retain the old successful snapshot until atomic publication of the new one.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: F26/F27/F02 consume this contract; final combined browser/native qualification remains a FUNC-G03 gate.

#### Completion Report

- status: implemented
- what was done: Shared lower inventory is integrated into graph, artifact catalog and fixed control-plane consumers: independent metadata tree and listing/read/index eligibility, gitignore/project policy precedence, versioned pins/cursors, profile-owned policy CAS, partial per-file failures and opt-in redacted display reads. Default analyzers and hard sensitive/link/root/private-key guards remain denied. The finite G02 projection is verified as a stricter subset of F28 authority.
- files touched / work locations: packages/contracts/project-inventory.ts; apps/local-service/src/project-inventory/service.mts; apps/local-service/src/code-index/sources.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/adapters/project-sources.ts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/storage/local-store.mts; apps/local-service/src/storage/sqlite-worker.mts; tests/web/project-inventory*.test.mts
- technical value delivered: One root/policy/revision and checked-read contract without duplicated scanner policy; metadata is not claimed as successful indexing.
- product value delivered: A per-file failure retains other permitted sources with explicit exclusions and partial coverage. Group UI acceptance follows in dependent slices.
- actual implementation date and time: 15-11-2026 20:10
- verification evidence: .tmp/func-g03/f28-verified-final.log:57/57,0skip; .tmp/func-g03/f28-final-typecheck.log:exit0; .tmp/func-g03/f28-lower-evidence.json:current lower15/15/source hashes; .tmp/func-g03/f28-consumer-red.log -> f28-consumer-green.log; .tmp/func-g03/f28-state-red.log -> f28-state-green.log; .tmp/func-g03/f28-cursor-red.log -> f28-consumers-final.log
- residual risks: Known credential filtering is bounded; git global/info excludes and tracked state are not git-status parity. Production browser/native tuple qualification and human acceptance are separate group/follow-up gates.
- follow-up: F26/F27/F02 consume this contract; final combined browser/native qualification remains a FUNC-G03 gate.
- Documentation impact: updated; docs/code-intelligence/inventory.md; docs/code-intelligence/inventory.en.md; docs/security/filesystem.md; docs/security/filesystem.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-29`

- Delivery group: `FUNC-G03`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-29 — Connect core discovery to project onboarding
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request for project file directory and managed scanning; multi-stage functional scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-27`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`
- Source: Core analyze_workspace and run_first_project_analysis provide discovery/first-run composition. The checked POST /projects does not call them: it currently uses only source inventory and code graph. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [plugins/product-agent-os/scripts/product_agent_os/discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py), [plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py). Sources were read in the 15.11.2026 analysis; runtime was not run.
- Short description: Connect core discovery to project onboarding.
- Technical value: Versioned read-only adapter to existing discovery/first-run analysis with provenance, limitations and invalidation.
- Product value: After adding a project, stack, structure, Control-plane gaps and grounded next steps are visible, not only graph node count.
- Scope: `apps/local-service/src/project-analysis/service.mts` (new planned file); `packages/contracts/project-analysis.ts` (new planned file); `apps/local-service/src/project-scans/service.mts` (new planned file); `apps/local-service/src/http/application.mts`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (new planned file); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/api/client.ts`; `tests/web/project-analysis.test.mts` (new planned file); `tests/web/single-window/project-files-browser-acceptance.mts` (new planned file). New paths are marked planned; a file introduced by another task is used only after that task.
- Architecture boundary: profile scan stage → bounded structured core adapter → project analysis view; analysis does not expand execution authority.
- Non-goals: Automatic project repair, creation of Control-plane, LLM audit, target build/tests and publication; unsupported completeness claims.
- Expected result: After adding a project, stack, structure, Control-plane gaps and grounded next steps are visible, not only graph node count. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build choose reuse of existing core discovery/first-run modules and deployment/runtime contract. Unavailable Python/adapter/version gives explicit unavailable; dependency installation and an alternative full scanner are not started automatically. AC2: Analysis runs as a separate F27 stage, uses agreed F28 inventory policy and returns schema version, source revision, stack/components, control-plane coverage and findings with sources/confidence/limitations. AC3: Discovered scripts/configs are analyzed only as data: project commands, tests, hooks, models or providers are not executed; target files are not created or repaired. Control-plane proposals remain proposals. AC4: Empty project, no Control-plane, Python-only, mixed stack and unsupported language get explainable results without invented completeness; timeout/error preserve the available tree and coverage already obtained. AC5: File, root or inventory policy changes make prior findings stale; retry and restart do not mix revisions. Findings are accessible from the selected project in RU/EN, linked to permitted file references and reveal no secrets. AC6: Discovery shows language/ORM/DB/schema file candidates with source and confidence for F14/F33/F34, without opening connections or running migrations. Project overview offers Files/Map/Database routes by capability; missing adapter is not substituted by third-party auto-install.
- Verification gates: `node --test tests/web/project-analysis.test.mts tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Expect exit0 and all scoped AC passing on synthetic fixtures. These commands are future work: new tests/harness do not exist yet. Browser acceptance uses an agreed runner protocol and disposable roots; exact flags are fixed before build. If core Python modules change, also run focused tests and the full TEST.md plugin/runtime route. Recheck runtime tuple before native acceptance after pinned sources change.
- Risks / approval gates: core_adapter_capability_contract_and_readonly_review_required; status=proposal_staged, design gate owner — architect + plugin-runtime-builder + builder + tester. Before build approve API/policy/state contract, source ownership and recovery. No provider/live calls, dependency installation or existing-profile changes without separate exact authorization.
- Complexity: high — API, filesystem boundary and handling incomplete results.
- Estimated execution time: 16–32 h, rough planning range; choose integration/packaging before build; not a schedule commitment.
- Agents: architect + plugin-runtime-builder + builder + tester; roles are proposed, subagents are not running. Change shared API/storage/UI files sequentially with owners of dependent tasks.
- Skills: implementation-planner for this planning; choose task-matching runtime/frontend/test skills at start. For Python implementation follow existing python-design-patterns/python-code-style guidance.
- Output artifacts: Read-only discovery integration and source-backed summary, capability/timeout/stale fixtures; reuse contract in existing architecture. Status is this group's JSON; evidence and Documentation impact are in this Completion Report; compact handoff is RUNLOG.md.
- Rollback: only own changes after checking drift; test schema/recovery changes on a disposable profile. Do not change target files; retain the old successful snapshot until atomic publication of the new one.
- Planning update GitHub/UI 15.11.2026: AC and dependencies F30–F34 updated; the addendum's shared UI/UX contract applies within affected scope, implementation has not started.
- Next step: No remaining work in this task; future consumers/packaging/performance retain their own tasks.

#### Completion Report

- status: implemented
- what was done: Core discovery runs as a durable scan stage through fixed Python -I -S -B and a bounded F28 projection; overview exposes actual core identity/source revision, stack/languages/control-plane/schema candidates, capabilities and stale/unavailable states. No target scripts, DB or providers execute.
- files touched / work locations: apps/local-service/src/project-analysis/service.mts; apps/local-service/src/project-analysis/bridge.py; apps/local-service/src/http/application.mts; apps/web/src/features/projects/ProjectAnalysis.tsx; tests/web/project-analysis.test.mts; tests/web/project-analysis-api.test.mts
- technical value delivered: Shared root/policy/revision contracts and final authority fences verified on current API/SQLite/FS/build/native fixtures.
- product value delivered: Partial and stale observations are explicit; execution limits are explained before dispatch while source data and drafts are preserved.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: No remaining work in this task; future consumers/packaging/performance retain their own tasks.
- Documentation impact: updated; docs/code-intelligence/discovery.md; docs/code-intelligence/discovery.en.md; docs/architecture/data-flow.md; docs/architecture/data-flow.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-30`

- Delivery group: `FUNC-G02`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-30 — Evaluate dependency-cruiser for JS/TS dependency graph
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request to move GitHub research into the plan with UI/UX and dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-14`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [sverweij/dependency-cruiser](https://github.com/sverweij/dependency-cruiser)
- Short description: Evaluate dependency-cruiser for JS/TS dependency graph.
- Technical value: Evaluate reuse of an import analyzer instead of extending the current lexical parser; agree JSON adapter and edge semantics.
- Product value: User and agent see verifiable file dependencies, cycles and a path to the change location.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Proposed paths; existing shared UI/API/storage files are changed sequentially.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; third-party cache is not the PAOS control-plane DB
- Non-goals: Implementation outside selected capabilities; changes to target/global configuration; provider/live DB calls, publication or installation under current planning. PoC does not mean production integration.
- Expected result: User and agent see verifiable file dependencies, cycles and a path to the change location. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before running pin version/commit, MIT and distribution licenses, Windows/Node compatibility, fixture corpus, current lexical graph baseline and time/RSS/response-size budgets; results are not inferred from README. AC2: Synthetic JS/TS fixtures cover ESM/CommonJS, tsconfig aliases, re-exports, cycles, missing imports, dynamic import and monorepo boundaries; import is not called a function call. Compare known expected edges to output: list false positives/negatives and unresolved. AC3: JSON adapter preserves normalized path/root identity, source revision, edge type/direction and evidence; respects the agreed F28 contract without depending on completion of its implementation. Configuration is passed by PAOS as data: target JS-config/scripts/hooks are not executed; target hashes do not change. AC4: An isolated prototype of the existing Map has Dependencies mode: file search, incoming/outgoing, type filter, path/cycle highlighting, file/line navigation and synchronized graph/list/Mermaid. Errors and unsupported are shown; scenario peer review is not human acceptance. AC5: Compare time, files/context volume and result correctness with baseline on identical change-location tasks; parser failure/timeout does not hide the tree. Deterministic benchmark requires no provider calls; model evaluation only with separate exact authorization. AC6: Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request. AC7: The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance.
- UI/UX scope: Before build prepare and agree wireframes and navigation map in the existing V3 design: project → Files, Map, Database; labels are refined during design review. For the affected screen define loading/empty/partial/error/unavailable/stale, progress/cancel/retry by capabilities, RU/EN, both themes, keyboard/focus, readable labels and an accessible table instead of requiring diagram reading. Project switch, back, filter and selected object do not mix data; source/revision/coverage are visible. PoC uses an isolated prototype; production UI is accepted in F14/F33/F34.
- Verification gates: Before execution pin executable commands and versions in Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. No command was run by current planning.
- Risks / approval gates: poc_protocol_and_graph_ui_design_required; Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.
- Complexity: high — source accuracy, process/data boundaries and UI consistency
- Estimated execution time: 12–20 h PoC; build separately in F14; rough_range_not_commitment, not a schedule commitment.
- Agents: architect + graph-cockpit-engineer + tester; roles are proposed, subagents are not running now
- Skills: Choose task-matching skills at start; current planning does not install or activate skills/plugins.
- Output artifacts: Result and receipts belong in this Completion Report, status in group JSON; update existing architecture/design/help according to actual scope.
- Rollback: Only own hunks after checking drift; disposable PoC artifacts are cleaned within agreed bounds, user processes are not terminated; prior snapshots remain until successful publication.
- Next step: F14: bounded import-only adapter + current lexical queries; semantic/call-path gap remains.

#### Completion Report

- status: implemented
- what was done: dependency-cruiser18.6.0: 10/10 imports vs lexical7/10; change tasks3/3 vs2/3; 17 engine scenarios +4 model tests. Import-only adapter and V3 prototype checked; production F14 planned. Decision: bounded_adopt_import_only.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; owning domain docs RU/EN.
- technical value delivered: versioned adapter proposal, reproducible measured decision and explicit rejected capabilities.
- product value delivered: verified isolated graph/list/Mermaid/evidence/source prototype; human usefulness not measured.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: FUNC-G02 results above; .tmp/func-g02/ engine receipts; combined unit22/22, browser22/22; scoped typecheck/build; actual candidate failures retained.
- residual risks: research PoC only; production integration and human acceptance remain unverified; F31 downstream cases not executed after admission rejection.
- follow-up: F14: import-only F30 + bounded lexical; semantic/call-path gap.
- Documentation impact: updated adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry and owning task records RU/EN; Control-Plane Sync updated.

### Task `PAOS-FUNC-31`

- Delivery group: `FUNC-G02`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-31 — Evaluate codebase-memory-mcp as an agent indexing engine
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request to move GitHub research into the plan with UI/UX and dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-14`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)
- Short description: Evaluate codebase-memory-mcp as an agent indexing engine.
- Technical value: Evaluate SQLite-backed index, multilingual relations, queries and management of a separate native process via a versioned adapter.
- Product value: Agent receives small relevant context and an explainable change path, while user sees the basis of search.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Proposed paths; existing shared UI/API/storage files are changed sequentially.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; third-party cache is not the PAOS control-plane DB
- Non-goals: Implementation outside selected capabilities; changes to target/global configuration; provider/live DB calls, publication or installation under current planning. PoC does not mean production integration.
- Expected result: Agent receives small relevant context and an explainable change path, while user sees the basis of search. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Pin version/commit/license and distribution dependencies, Windows packaging, supported languages/relation types, workload and budgets. Comparison to current search uses the same ground-truth fixtures and tasks as F30; F30 need not finish first. AC2: Test search/definition/references/call path/impact and related tests only for claimed capabilities; publish measured precision/recall, unresolved and unsupported. Bounded responses provide file/line evidence, revision, truncation/pagination; stale index is not presented as current. AC3: Measure cold/incremental indexing, rename/delete/branch-like change, cancel/retry/restart, two projects, memory/disk and latency; SQLite/cache/locks belong to the engine and are not opened by PAOS as an unofficial writable API. AC4: On a disposable profile demonstrate daemon lifecycle/cleanup, timeout and child-process ownership; investigate account-wide coordination and another build/cache conflict. Do not terminate a user's daemon or change global MCP/skills/hooks/PATH, download models or send code externally. If isolation is incompatible with PAOS, result is bounded_adopt/reject, not a guard bypass. AC5: Map prototype includes symbol search, callers/callees/path/impact, explanation panel and source navigation; unavailable engine, partial coverage, stale and exceeded budget states are visible. UI contract does not depend on engine internal tables; evaluate reuse of existing PAOS graph UI. AC6: Comparative report defines F30/F31 roles: one selected backend or explicit language composition without duplicate/conflicting revisions. Before integration the engine respects F28 inventory policy; reject an option unable to restrict sensitive-file indexing. AC7: Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request. AC8: The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance.
- UI/UX scope: Before build prepare and agree wireframes and navigation map in the existing V3 design: project → Files, Map, Database; labels are refined during design review. For the affected screen define loading/empty/partial/error/unavailable/stale, progress/cancel/retry by capabilities, RU/EN, both themes, keyboard/focus, readable labels and an accessible table instead of requiring diagram reading. Project switch, back, filter and selected object do not mix data; source/revision/coverage are visible. PoC uses an isolated prototype; production UI is accepted in F14/F33/F34.
- Verification gates: Before execution pin executable commands and versions in Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. No command was run by current planning.
- Risks / approval gates: poc_daemon_isolation_and_agent_query_design_required; Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.
- Complexity: high — source accuracy, process/data boundaries and UI consistency
- Estimated execution time: 20–36 h PoC; integration separately in F14; rough_range_not_commitment, not a schedule commitment.
- Agents: architect + graph-cockpit-engineer + tester; roles are proposed, subagents are not running now
- Skills: Choose task-matching skills at start; current planning does not install or activate skills/plugins.
- Output artifacts: Result and receipts belong in this Completion Report, status in group JSON; update existing architecture/design/help according to actual scope.
- Rollback: Only own hunks after checking drift; disposable PoC artifacts are cleaned within agreed bounds, user processes are not terminated; prior snapshots remain until successful publication.
- Next step: F14: bounded import-only adapter + current lexical queries; semantic/call-path gap remains.

#### Completion Report

- status: implemented
- what was done: codebase-memory-mcp0.12.1 rejected before index admission; 12 integrity/admission/preservation checks +3 unit tests. Downstream cases not_executed_after_failed_admission with null metrics; unavailable UI and separate unmeasured call-contract fixture checked. Decision: reject_current_windows_workspace_profile.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; owning domain docs RU/EN.
- technical value delivered: versioned adapter proposal, reproducible measured decision and explicit rejected capabilities.
- product value delivered: verified isolated graph/list/Mermaid/evidence/source prototype; human usefulness not measured.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: FUNC-G02 results above; .tmp/func-g02/ engine receipts; combined unit22/22, browser22/22; scoped typecheck/build; actual candidate failures retained.
- residual risks: research PoC only; production integration and human acceptance remain unverified; F31 downstream cases not executed after admission rejection.
- follow-up: F14: import-only F30 + bounded lexical; semantic/call-path gap.
- Documentation impact: updated adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry and owning task records RU/EN; Control-Plane Sync updated.

### Task `PAOS-FUNC-32`

- Delivery group: `FUNC-G02`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-32 — Evaluate tbls for DB schema extraction and Mermaid ERD
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request to move GitHub research into the plan with UI/UX and dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: none
- Blocks: `PAOS-FUNC-33`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [k1LoW/tbls](https://github.com/k1LoW/tbls), [www.sqlite.org/pragma.html](https://www.sqlite.org/pragma.html)
- Short description: Evaluate tbls for DB schema extraction and Mermaid ERD.
- Technical value: Evaluate an external JSON/Mermaid schema adapter against built-in SQLite introspection and pin the schema snapshot contract.
- Product value: Obtain a reliable table map without manual drawing or reading user rows.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Proposed paths; existing shared UI/API/storage files are changed sequentially.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; third-party cache is not the PAOS control-plane DB
- Non-goals: Implementation outside selected capabilities; changes to target/global configuration; provider/live DB calls, publication or installation under current planning. PoC does not mean production integration.
- Expected result: Obtain a reliable table map without manual drawing or reading user rows. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Pin version/commit/MIT/dependency licenses, Windows distribution, minimum SQLite-first scope and budgets; compare tbls JSON/Mermaid against metadata introspection of the existing SQLite driver. PostgreSQL and other DBMS are separate capability targets, not automatic scope. AC2: Synthetic SQLite covers PK/FK, composite FK, UNIQUE/index, views, nullable/generated columns, self-reference and missing FK. Compare object and edge lists with ground truth; format/driver limitations and inferred relations are not hidden. AC3: Use an explicitly selected read-only fixture/consistent snapshot; row data, credentials and DSN do not enter logs/output. Test locked/WAL/change-during-read, inaccessible and corrupt files; connection does not create a missing DB, migrate it or execute project config/extensions/hooks. AC4: Result contains source kind, schema fingerprint/revision, tables/columns/keys/indexes/views, coverage and warnings; canonical JSON and Mermaid agree. Test name escaping and ERD size limits, no HTML/script execution. AC5: Isolated prototype of the future Database section shows source, ERD and object table, table/column selection, search/filter and explicit no-database/unsupported/stale/error. Mermaid export requires no external service; tiny Mermaid is checked for required ERD semantics. AC6: Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request. AC7: The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance.
- UI/UX scope: Before build prepare and agree wireframes and navigation map in the existing V3 design: project → Files, Map, Database; labels are refined during design review. For the affected screen define loading/empty/partial/error/unavailable/stale, progress/cancel/retry by capabilities, RU/EN, both themes, keyboard/focus, readable labels and an accessible table instead of requiring diagram reading. Project switch, back, filter and selected object do not mix data; source/revision/coverage are visible. PoC uses an isolated prototype; production UI is accepted in F14/F33/F34.
- Verification gates: Before execution pin executable commands and versions in Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. No command was run by current planning.
- Risks / approval gates: poc_database_readonly_and_erd_ui_design_required; Result is adopt / bounded_adopt / reject with receipts, pinned version/commit/license, supported platforms and baseline comparison. A justified rejection completes the PoC as research but does not implement the feature; downstream design selects an alternative or records a blocker, without silent fallback. Installation/execution is not authorized by the current planning-only request.
- Complexity: high — source accuracy, process/data boundaries and UI consistency
- Estimated execution time: 12–20 h PoC; integration separately in F33; rough_range_not_commitment, not a schedule commitment.
- Agents: architect + graph-cockpit-engineer + tester; roles are proposed, subagents are not running now
- Skills: Choose task-matching skills at start; current planning does not install or activate skills/plugins.
- Output artifacts: Result and receipts belong in this Completion Report, status in group JSON; update existing architecture/design/help according to actual scope.
- Rollback: Only own hunks after checking drift; disposable PoC artifacts are cleaned within agreed bounds, user processes are not terminated; prior snapshots remain until successful publication.
- Next step: F33: explicit node:sqlite metadata adapter proposal; production integration planned.

#### Completion Report

- status: implemented
- what was done: tbls1.96.1: 26 observations =23 positive +3 candidate failures (generated omission, valid identifier failure, missing DB creation). Explicit node:sqlite read-only metadata alternative, effective nullable fixed;6 unit tests; schema UI/export checked. Decision: reject_authoritative_sqlite_metadata.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; owning domain docs RU/EN.
- technical value delivered: versioned adapter proposal, reproducible measured decision and explicit rejected capabilities.
- product value delivered: verified isolated graph/list/Mermaid/evidence/source prototype; human usefulness not measured.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: FUNC-G02 results above; .tmp/func-g02/ engine receipts; combined unit22/22, browser22/22; scoped typecheck/build; actual candidate failures retained.
- residual risks: research PoC only; production integration and human acceptance remain unverified; F31 downstream cases not executed after admission rejection.
- follow-up: F33: explicit node:sqlite metadata adapter; production integration planned.
- Documentation impact: updated adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry and owning task records RU/EN; Control-Plane Sync updated.

### Task `PAOS-FUNC-33`

- Delivery group: `FUNC-G04`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-33 — Add a DB map and project Database section
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request to move GitHub research into the plan with UI/UX and dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-28`, `PAOS-FUNC-32`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`, `PAOS-FUNC-34`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [k1LoW/tbls](https://github.com/k1LoW/tbls), [www.sqlite.org/pragma.html](https://www.sqlite.org/pragma.html)
- Short description: Add a DB map and project Database section.
- Technical value: Versioned schema snapshots, schema diff and a provenance/freshness-aware read-only adapter for the chosen source.
- Product value: Users browse tables and relations, understand source and freshness of the schema, and navigate to its definition.
- Scope: `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/storage/migrations/schema.mts`; `apps/local-service/src/project-scans/service.mts`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`; `packages/contracts/database-map.ts` (new planned file); `apps/local-service/src/database-map/service.mts` (new planned file); `apps/web/src/features/database/DatabaseExplorer.tsx` (new planned file); `tests/web/database-map.test.mts` (new planned file); `tests/web/single-window/database-map-browser-acceptance.mts` (new planned file). Proposed paths; existing shared UI/API/storage files are changed sequentially.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; third-party cache is not the PAOS control-plane DB
- Non-goals: Implementation outside selected capabilities; changes to target/global configuration; provider/live DB calls, publication or installation under current planning. PoC does not mean production integration.
- Expected result: Users browse tables and relations, understand source and freshness of the schema, and navigate to its definition. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build select adapter, supported sources and budgets using F32; missing backend selection remains a blocker. Distinguish PAOS's own DB from the analyzed project DB. Discovering a candidate in the tree does not open it automatically: user selects a permitted source; external/live/credentials require exact authorization. AC2: Contract distinguishes actual DB schema, static ORM/migrations and proposed relations. An unapplied migration is not presented as the current DB; executing migrations/project code/extensions is forbidden. SQLite-first read-only schema extraction reads no rows and does not create/change the DB; PostgreSQL scope is not inferred from tbls support. AC3: Add Database to project navigation with Schema and Changes tabs; Schema offers ERD/table mode, search, filters, table/column details, PK/FK/index/views and navigation to allowed schema/migration source. Settings retains registration and source selection, not a second independent browser. AC4: ERD and table show one revision; composite FK and direction are correct, inferred relations differ from declared. Node selection syncs details/list, large schemas provide bounded subgraph and warning, Mermaid export escapes names, reveals no secrets and reports filters/coverage. AC5: Changes compares two compatible snapshots: added/removed/changed objects; rename without proof is shown as add/remove or hypothesis. Missing baseline is explicit empty; source/policy drift marks stale, schema fingerprint and observation time are visible. AC6: F27 database_schema stage has independent progress/cancel/retry/recovery/partial/error; failure preserves the previous successful snapshot marked stale and does not block Files/code. Unselected/missing DB is not_configured/none_found, not endless loading. Reject late responses from another project/revision. AC7: Pass F32 API/adapter and browser scenarios on disposable fixtures: RU/EN, both themes, keyboard/focus, table alternative, deep link/back, restart and project switching. Target and control files remain unchanged before/after; no sensitive DSN/rows in UI/export/logs; runtime evidence is build-bound. AC8: On F20 workload measure schema extraction, cold/warm view, large ERD, memory and response size; budget deviations have bounded outcomes. Update F24/F25 docs/capabilities for actually implemented scope; UI mock does not close acceptance. AC9: The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance.
- UI/UX scope: Before build prepare and agree wireframes and navigation map in the existing V3 design: project → Files, Map, Database; labels are refined during design review. For the affected screen define loading/empty/partial/error/unavailable/stale, progress/cancel/retry by capabilities, RU/EN, both themes, keyboard/focus, readable labels and an accessible table instead of requiring diagram reading. Project switch, back, filter and selected object do not mix data; source/revision/coverage are visible. PoC uses an isolated prototype; production UI is accepted in F14/F33/F34.
- Verification gates: Adapter/API tests, UI type-check/build and synthetic browser acceptance on selected runtime; exact commands are fixed before build. New harness does not exist yet.
- Risks / approval gates: database_source_adapter_and_ui_design_required; After PoC select backend and agree architecture/UI contract; build does not start without this.
- Complexity: high — source accuracy, process/data boundaries and UI consistency
- Estimated execution time: 16–24 h design; refine build after F32; rough_range_not_commitment, not a schedule commitment.
- Agents: architect + builder + graph-cockpit-engineer + tester; roles are proposed, subagents are not running now
- Skills: Choose task-matching skills at start; current planning does not install or activate skills/plugins.
- Output artifacts: Result and receipts belong in this Completion Report, status in group JSON; update existing architecture/design/help according to actual scope.
- Rollback: Only own hunks after checking drift; disposable PoC artifacts are cleaned within agreed bounds, user processes are not terminated; prior snapshots remain until successful publication.
- Next step: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.

#### Completion Report

- status: implemented
- what was done: Added explicit SQLite source Settings, purpose-specific admission, native SHARE_READ lease, schema-only authorizer/extractor, profile CAS/two snapshots/diff, an independent F27schema stage and production Database Schema/Changes/ERD/list/details UI.
- files touched / work locations: packages/contracts/database-map.ts; apps/local-service/src/database-map/; apps/local-service/src/project-inventory/service.mts; apps/local-service/src/project-scans/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/database/; apps/web/src/ui/App.tsx; tests/web/database-map.test.mts; tests/web/database-source-admission.test.mts; tests/web/database-map-api.test.mts
- technical value delivered: Native write/rename/reparse/WAL/row/extension guards, late-selection fences and retained stale metadata are verified without target mutation.
- product value delivered: Selected schema, keys, indexes, views and changes are accessible through RU/EN UI/API without row reads.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; native34/34 initial backend, final full658 includes new late-source-revocation regression and shared watchdog; actual readOnly adapter/API/private-source stages; profile DB excluded; target hashes and directory contents preserved; 200 unique objects, four revision-consistent pages of 50; current ERD timings in .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; prior 100-object/1969 ms failure retained; browser realcancel/retry/writerfailure/staleDDLdiff/restart/2projectlatefence/deepanchor; corrected390px header/scroll table actualscreenshots
- residual risks: Windows/offline project-local SQLite only, no WAL/sidecars/real credentials/remote DB/rows. Views/virtual tables partial; rename means add/remove.128MiB stat/200 objects/512KiB output; UI50 per page. Browser aggregate RSS is not a qualified whole-system peak.
- follow-up: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.
- Documentation impact: updated; docs/db/erd.md; docs/db/erd.en.md; docs/code-intelligence/adapters.md; docs/code-intelligence/adapters.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/product/capabilities.md; docs/product/capabilities.en.md; scoped source checks passed.

### Task `PAOS-FUNC-34`

- Delivery group: `FUNC-G04`; the group does not replace Depends on or the original AC.
- Task: PAOS-FUNC-34 — Link code to tables and show change impact
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner request to move GitHub research into the plan with UI/UX and dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-14`, `PAOS-FUNC-33`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [sverweij/dependency-cruiser](https://github.com/sverweij/dependency-cruiser), [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp), [k1LoW/tbls](https://github.com/k1LoW/tbls)
- Short description: Link code to tables and show change impact.
- Technical value: Add provenance-aware code→query/ORM→table edges resolved in compatible code/schema revisions and bounded impact queries.
- Product value: User and agent see which code reads or changes a table and what to check when its schema changes.
- Scope: `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/impact/service.mts`; `apps/local-service/src/database-map/service.mts`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/features/database/DatabaseExplorer.tsx`; `apps/web/src/features/files/ProjectFiles.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`; `packages/contracts/code-database-links.ts` (new planned file); `apps/local-service/src/code-database/service.mts` (new planned file); `tests/web/code-database-links.test.mts` (new planned file); `tests/web/single-window/code-database-browser-acceptance.mts` (new planned file). Proposed paths; existing shared UI/API/storage files are changed sequentially.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; third-party cache is not the PAOS control-plane DB
- Non-goals: Implementation outside selected capabilities; changes to target/global configuration; provider/live DB calls, publication or installation under current planning. PoC does not mean production integration.
- Expected result: User and agent see which code reads or changes a table and what to check when its schema changes. Confirmation is the observable scenarios below, separate from human acceptance.
- Acceptance criteria: AC1: Before build choose a bounded language/SQL/ORM matrix based on F30/F31/F32; include code call paths only with confirmed semantics, import edges do not substitute for CALLS. Fix ground-truth cases and precision/recall thresholds before measurement. AC2: Relation stores file/symbol/line span, query or model evidence, table identity/source, operation read/write/schema/unknown, extraction method/confidence and code+schema revisions. Dynamic SQL, naming heuristics, aliases and untraceable calls remain inferred/unresolved; unknown is not treated as absence of dependency. AC3: Test raw SQL, chosen ORM, joins/aliases, identical table names in different sources, rename/drop, generated/dynamic query and unsupported language. Code/queries are not executed; secrets/DB rows are not extracted; precision/recall and limitations are presented per supported type. AC4: Add Code usage tab to Database: table → read/write locations → file/line; existing Map gets DB-link filter and path/impact panel. File reader supports navigation to linked tables. Selection/deep link/back/filter stay within project; arbitrary relations are not drawn as confirmed. AC5: User switches confirmed/inferred and read/write/unknown, opens edge evidence and sees incomplete impact. Accessible table/list duplicates graph meaning; RU/EN, both themes, keyboard/focus, empty/unsupported/partial/error/stale and large results are tested in browser. AC6: Agent queries return bounded source-backed paths and test candidates, truncation/cursors and both revisions; source rename/delete/change invalidates only the compatible snapshot. Mixing code/schema from different projects or stale revisions is forbidden; rebuild/restart/cancel/retry are tested. AC7: Compare locating changes on agreed tasks without and with relations: correctness, missed affected files/tests, context and time; no promises of complete runtime call graph. F20 budgets and F27/F28 guardrails are met; one analyzer failure does not block tree and schema map. AC8: Documentation explains schema ERD versus code-to-table impact; release claims and capability states align with F24/F25. Closure requires working UI/API/agent-contract integration, not only a schema or prototype. AC9: The shared F30–F34 UI/UX addendum contract is met within this task's PoC prototype or production slice; design-review and scoped browser-check results are recorded separately from human acceptance.
- UI/UX scope: Before build prepare and agree wireframes and navigation map in the existing V3 design: project → Files, Map, Database; labels are refined during design review. For the affected screen define loading/empty/partial/error/unavailable/stale, progress/cancel/retry by capabilities, RU/EN, both themes, keyboard/focus, readable labels and an accessible table instead of requiring diagram reading. Project switch, back, filter and selected object do not mix data; source/revision/coverage are visible. PoC uses an isolated prototype; production UI is accepted in F14/F33/F34.
- Verification gates: Adapter/API tests, UI type-check/build and synthetic browser acceptance on selected runtime; exact commands are fixed before build. New harness does not exist yet.
- Risks / approval gates: code_database_semantics_and_impact_ui_design_required; After PoC select backend and agree architecture/UI contract; build does not start without this.
- Complexity: high — source accuracy, process/data boundaries and UI consistency
- Estimated execution time: 20–32 h design; build after language/ORM scope; rough_range_not_commitment, not a schedule commitment.
- Agents: architect + builder + graph-cockpit-engineer + tester; roles are proposed, subagents are not running now
- Skills: Choose task-matching skills at start; current planning does not install or activate skills/plugins.
- Output artifacts: Result and receipts belong in this Completion Report, status in group JSON; update existing architecture/design/help according to actual scope.
- Rollback: Only own hunks after checking drift; disposable PoC artifacts are cleaned within agreed bounds, user processes are not terminated; prior snapshots remain until successful publication.
- Next step: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.

#### Completion Report

- status: implemented
- what was done: Added static literal JS/TS/SQL and a Prisma subset, selected-source-only confirmation, both-revision/HMAC/32KiB queries, an independent F27code_database stage, Database Code usages/Map DB network/Files related tables and a claimed App-agent project-query port.
- files touched / work locations: packages/contracts/code-database.ts; apps/local-service/src/code-database/; apps/local-service/src/runtime/app-agent-channel.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/web/src/features/database/CodeDatabaseUsages.tsx; apps/web/src/features/files/ProjectFiles.tsx; tests/web/code-database-*.test.mts; tests/web/database-map-api.test.mts
- technical value delivered: Precise source/confidence/operation/span pins, native child containment, late-CAS/lease guards and bounded safe context replace guessed relationships.
- product value delivered: Users can find code/test candidates for a table, navigate source evidence and distinguish confirmed from inferred/unresolved.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; ground truth24/24; confirmed literalSQL8/8 andPrisma2/2 precision1/recall1 forliteraldenominators; rootshadowURL/TSparam/nestedDELETE regressions included; actual owned childnative stackfailure3221225725 contained,parentalive; deadline/cancel/bothpins/HMAC/source/policy/CAS/400-link32KiB pagination; production API + private claimed synthetic worker roundtrip; post-read/post-scope lease expiry rejects; no model/provider/credentials; static-search comparison finds missed ORM files; structured context/time notgenerally smaller/faster; literalproxy limits recorded; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.
- residual risks: Prisma v6 static subset/JS/TS/SQL only; dynamic/env/untraced/foreign-source cases remain uncertain. No SQL/ORM execution, rows/DSNs or runtime call graphs. Queries require current code+schema pins. No human/model-superiority or general time/context-saving claim.
- follow-up: No required work remains within this card; measured limits are retained. The next group and human/release acceptance remain separate.
- Documentation impact: updated; docs/code-intelligence/queries-impact.md; docs/code-intelligence/queries-impact.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/backend/modules.md; docs/backend/modules.en.md; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/product/capabilities.md; docs/product/capabilities.en.md; scoped source checks passed.
