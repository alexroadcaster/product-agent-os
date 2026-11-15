# Product-Agent OS — documentation architecture and backlog

Source status: repository_source / current_source_inspection / owner_requested_planning; subsystem documentation implementation planned, DG01/DG02/DG03/DG04 docs_static_verified; remaining subsystem work planned.
Date: 15.11.2026. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Analysis results

The baseline docs tree contains 316 Markdown files, including RU/EN and archives. Its structure primarily documents Codex, methodologies and the Python plugin. This is a useful knowledge base, but not complete documentation of the current Web/desktop application. docs/planning was empty. We found and relocated 42 standalone plans/backlogs/task-state files, updating references. The [relocation map](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/relocation-2026-11-15.json) records former/current paths and before/after hashes.

The inspection covered 57 top-level research MD/JSON files, legacy plans and task-state/specs, and design implementation plans; references were searched across 2297 text files. Research fixtures and reports are not task queues merely because they mention task IDs. Root AGENTS/PLAN/TEST/EVALS/RUNLOG retain control-plane ownership; packaged templates and synthetic target fixtures are not this project's plans. Other chats' session markers and private historical reviews are unchanged: old references can be located through the migration map. Historical receipts are not presented as newly executed checks.

### Confirmed observations

| Area | Existing implementation/documentation | Gap |
| --- | --- | --- |
| Backend | [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts) wires task manager, artifacts, team, code index, scheduler, recipes and decisions; storage/runtime modules are separate | No unified PAOS Web module/lifecycle/API guide; methodologies/backend describes a method, not actual architecture |
| Frontend | [apps/web/src/ui/App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/App.tsx), features, API client, V3 design and [apps/web/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/README.md) | No connected screens/state/dataflow/design-to-code map; README mixes current instructions and history |
| DB | [apps/local-service/src/storage/migrations/schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/migrations/schema.mts) defines 16 CREATE TABLE/VIRTUAL TABLE statements, including entities/events/outbox/FTS; SQLite worker/restore/search | Need ERD, tables/invariants/authority and migration/backup contracts; target-project schema F33 is distinct from PAOS SQLite |
| AI/LLM Web | [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts) contains codex_app_agent/local_api_byok and prohibits implicit fallback | Runtime routes/connection/credentials/limits are scattered across research and receipts |
| Retrieval/RAG | [apps/local-service/src/storage/search-queries.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/search-queries.mts) uses SQLite FTS5; [plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py) is a separate deterministic semantic cache | Web search cannot be called production RAG; this audit did not establish explicit integration between the two paths |
| Providers/proposals | [plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py) and [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) define gates; the default does not call live providers | Need a deterministic/staged/live-approved capability matrix; a module's presence does not prove activation |
| Guides | docs/product-agent-os already covers graph/governance/formation/CLI/privacy/evals; docs/agent-systems and methodologies provide general knowledge | Reuse and connect owners instead of copying every page into new empty directories |

This is a static source/docs audit, not runtime acceptance; the audit made no provider/network calls. RAG/LLM names among task components do not establish a RAG runtime.

## Proposed docs structure

Directory names remain lowercase, matching the repository. AI groups agents/llm/rag beneath one parent instead of four independent root sections. Create directories with substantive pages through the tasks below. The initial audit performed only planning relocation and backlog authoring; the current DG01 separately authorizes repair.

```text
docs/
  planning/                 # actual plans, backlogs, task state and migration map
  product/                  # current product, domains, capabilities, user journeys
  architecture/decisions/   # system structure and ADRs
  backend/                  # local service and server modules
  api/                      # HTTP/events/shared contracts
  frontend/                 # UI/UX, navigation, state and design-to-code
  db/                       # PAOS SQLite, schema/ERD, migration, backup
  ai/
    agents/                 # orchestration, tools, sessions, approvals
    llm/                    # routes, prompts, models/providers, budgets
    rag/                    # lexical/semantic retrieval and actual limitations
  code-intelligence/        # discovery, inventory, graph, impact, adapters
  security/                 # product trust boundaries and data protection
  testing/                  # tests/evals and evidence map
  operations/               # launch, profiles, update/rollback, troubleshooting
  product-agent-os/         # existing plugin/operator guides
  diagrams/                 # the existing shared atlas
  codex/ methodologies/     # general knowledge, separate from implementation
  agent-systems/ prompting/ # general approaches, not PAOS implementation evidence
  sources/ insights/        # sources and research notes
  web/                      # existing user guides, linked from frontend/operations
  superpowers/specs/        # historical design/evidence, not the live task backlog
```

## What was moved and what remains

| Class | Action |
| --- | --- |
| 6 research files: FUNC MD/JSON, Web MD/JSON, audit remediation and ordinary-route plan | Moved to docs/planning, preserving cards/statuses |
| 20 legacy Markdown plans, including EN | Moved from docs/superpowers/plans to docs/planning |
| 6 Track 8/9/10 RU/EN backlogs | Moved from docs/sources to docs/planning; archive notices retained |
| 5 task-group/next-task JSON and 2 task-plan TXT files | Moved from docs/superpowers/specs to docs/planning; evidence packets stay in specs |
| 3 design implementation plans | Moved to docs/planning with date/version filenames; images, design and receipts stay with design |
| PRD, architecture and auth/storage research | Remain in research for now; DOCS-02/03/07/09/12 extract current chapters into canonical domain sections and preserve historical rationale |
| Methodologies/backend/frontend/database/LLM-AI-RAG | Remain methodologies; implementation guides link to them but describe actual code |
| Plugin guides, diagram atlas and security/eval pages | Reused with explicit ownership; DOCS-03/08/10/11/12/13/15 add missing implementation-specific details |
| Execution reports/results, audit findings and requirements history | Remain research/evidence linked from current guides; a report listing completed tasks is not renamed into a new plan |

## Sequence and connection to FUNC

The seven groups below own the current execution order: DG01 first, then task-specific dependencies. The functional-plan mapping is preserved: G01→backend/frontend/API; G02→code-intelligence/AI; G03→backend/API/frontend; G04→DB/code-intelligence/retrieval; G05→AI/security; G06→operations/testing; G07→product/testing/navigation. Functional groups and statuses do not change.

## Documentation implementation groups — 15.11.2026

Current status: DG01–DG04 **completed / docs_static_verified**; DOCS-01–07 **implemented**, DOCS-13/16 **in_progress** until B; other 7 tasks and DG05–DG07 **planned**. IDs, original dependencies, scope and AC preserved.

### Stage and dependency rules

DOCS-13 and DOCS-16 each have two stages within their existing card: **13/A, 16/A** repair current relocation problems; **13/B, 16/B** perform the main work and full closure. Stage labels are not new task IDs or another status authority. There are 16 tasks and 18 executable stages: 14 ordinary tasks plus four stages of two tasks. DG06 owns full DOCS-13 closure; DG07 owns full DOCS-16 closure.

For ordinary tasks, Depends on remains an entry requirement. For DOCS-13/16 it is an entry requirement for B and full closure; A checks existing documentation without waiting for future domain sections. This explicitly clarifies the previously ambiguous early-repair allowance rather than deleting dependencies. Record A evidence inside the parent card; the parent remains in_progress until B and all original AC are complete. Stages A are completed; stages B remain planned.

**DG01 is the mandatory first stage:** DG02–DG07 cannot begin execution before its acceptance. Thereafter, individual task dependencies determine entry: group numbering does not add a wait for every earlier-numbered group to finish.

| Group | Tasks/stages | Entry and internal sequence | Outcome and exit gate |
| --- | --- | --- | --- |
| **DG01 — relocation repairs** | **DOCS-16/A**, **DOCS-13/A** | First, without future domain docs; two independent streams with coordinated check ownership | Restore repository/site links and anchors; handle links outside docs and language links; close eight EN gaps with substantive translations. Align historical assertions with the current contract without enabling hooks or weakening guards for green tests. Isolated strict build, source, site and archive checks pass; a remaining blocking failure prevents closure |
| **DG02 — structure, product and architecture** | **DOCS-01**, **DOCS-02**, **DOCS-03** | After DG01: 01 → 02 → 03 | Section owners, current product/domain model, architecture boundaries and ADRs; distinguish Web/desktop, Python plugin and planned capabilities; meet all three cards' original AC |
| **DG03 — backend, API and data** | **DOCS-04**, **DOCS-05**, **DOCS-07** | After 03: 04 → 05 → 07; expose 05 immediately to DG05 | Local-service, HTTP/events/errors and SQLite/ERD/migrations/backup docs match code/tests; distinguish PAOS SQLite from target DB F33 |
| **DG04 — frontend and UI/UX** | **DOCS-06** | After 01/02/03; parallel with DG03 | Map navigation/screens/state/components/design/a11y; separate actual and future Files/Map/Database states. DOCS-05 owns shared API facts without a conflicting second specification |
| **DG05 — AI, LLM, retrieval and graphs** | **DOCS-08**, **DOCS-09**, **DOCS-10**, **DOCS-11** | 08 after 03/05; 08 → 09; 10 after 07/08/09; 11 after 03/05/10 | Align orchestration/routes/providers, search/retrieval/RAG and discovery/graph/impact; separate existing and PoC/planned paths. 08 may run alongside 07; DG04 is not a prerequisite |
| **DG06 — security and verifiability** | **DOCS-12**, **DOCS-13/B** | 12 after 03/05/07/08; 13/B after 13/A and 04/05/06/07/08; independent work allowed | Security/privacy/trust-boundary guide and tests/evals/evidence map agree with subsystem owners. Close DOCS-13 only after A+B and all original AC; no need to wait for all DG05 |
| **DG07 — operations, plugin and final integration** | **DOCS-14**, **DOCS-15**, **DOCS-16/B** | 14 after 04/07/12/13; 15 after 01/03/08/11/13; 14 and 15 independent when inputs are ready; 16/B after 16/A and full 01–15 closure | Connect operations/rollback/troubleshooting and Python plugin guides to architecture. Final owner/update matrix, FUNC G01–G07 links, RU/EN navigation and strict/site/source checks accept the full set without reintroducing DG01 errors |

### Early and final stage scope

- **DOCS-16/A:** repair consequences of moving 42 files: repository/published links, anchors/redirect policy, EN sibling links, eight missing translations, search/sitemap parity and a reproducible isolated build. Preserve task state, migration provenance and historical receipts. Do not hide failures by disabling validation or using fake translations.
- **DOCS-13/A:** compare the historical PostToolUse assertion and other relocation failures with the current contract; change outdated test expectations only with evidence and retain necessary checks. Hooks/trust remain outside this repair; activation is not authorized. If an error requires such a change, keep the group open with an explicit blocker.
- **DOCS-13/B:** document test/eval maps, synthetic/runtime/human evidence and verification routes. Include A as dated earlier repair, not invented repeated verification.
- **DOCS-16/B:** integrate all new sections, document owners and feature delivery; recheck the complete current set. First-group success does not prove the future site's readiness.

DG01 criteria supplement the early portion of DOCS-13/16. DG02–DG07 criteria do not replace cards: closure requires every included task's AC. Full DG07 closure requires DG01–DG06 outcomes; it does not imply product readiness or automatic publication.

### Parallel work and file ownership

After DG02, DG03 and DG04 are separate branches. After DOCS-05, start DOCS-08/09 alongside DOCS-07; DOCS-10 waits for both. Once DOCS-08 and DB/frontend inputs are ready, DG06 may start while DG05 finishes retrieval/graph docs. DOCS-14 may start before DOCS-11/15 if its own prerequisites are closed.

Ownership: DG03 backend/api/db; DG04 frontend; DG05 ai/code-intelligence; DG06 security/testing; DG07 operations/product-agent-os and final integration. Update shared mkdocs.yml, indexes, registries, PLAN/RUNLOG, diagram atlas and related checks sequentially through one integration owner. This grouping itself did not launch a team. Independent branches enable acceleration; no numeric time saving is estimated.

### Grouping verification

This section owns sequencing. The card table below retains original dependencies; staged exceptions for DOCS-13/16 are defined here and in the cards. Check coverage of all 16 IDs, no new/lost cards, exactly one group per stage, an acyclic 18-stage graph, the DG01 prerequisite for subsequent work and preserved original AC/status/dependencies. Grouping does not change earlier failed build/archive/site receipts.

Grouping checks on 15.11.2026: validate_task_matrix passed; source-docs unittest 3/3 passed (0.669s); check_docs and git diff --check passed. Comparing before/after cards: 16/16 remained byte-identical after removing only added Delivery group/Execution stages fields; all were planned at that time. Seven groups/18 unique stages and the DAG with mandatory DG01 entry passed. Review: self_review. Control-plane sync: PLAN/RUNLOG updated; REQUIREMENTS/TEST/EVALS/registries no_change_needed because requirements, source claims and verification routes were unchanged. MkDocs/site/archive were not rerun during grouping; earlier results were not promoted.

## DG04 — implementation results {#dg04-results}

Status: **completed / docs_static_verified**; DOCS-06 **implemented**. Date: 15-11-2026 16:57 Europe/Moscow. Source snapshot `ad78d5d15aced23febae90d319f2aba00bd64d0b`. Original AC/Scope/Depends on/Blocks preserved.

| Criterion | Completed |
| --- | --- |
| AC1 | [Navigation](../frontend/navigation.md): all 15 App sections, transitions and onboarding; [state](../frontend/state-management.md): API, polling, late responses, message/task drafts and ACK; [components](../frontend/components.md), themes and RU/EN with source/test references |
| AC2 | [Design system](../frontend/design-system.md) routes to DESIGN and V3 assets; no copied token/screenshot catalog, design ownership preserved |
| AC3 | Files/Map/Database/usages F26–F34 planned; [accessibility](../frontend/accessibility.md) separates source mechanisms, historical 0029/V3 receipts, desktop scope and human/WCAG gaps |
| AC4 | [Frontend index](../frontend/index.md) and five guides, 6 complete RU/EN pairs: metadata/owner/scope/version/sources/tests/limits; nav/registry and control plane synchronized |

Current checks: check_docs passed; source suite 3/3 + translation-card regression 1/1; RU/EN matrices passed, 16 cards each; strict isolated MkDocs and i18n postprocess passed; site 7/7; affected HTML links/anchors without errors; pinned source references and all six RU/EN source sets match; all 15 App sections present in both languages; git diff --check passed. Local receipts: .docs-tools/reports/dg04.

Review: self_review + separate_reused_context scoped design/components/accessibility review by dg04_navigation_state; tester_verdict=closed_allowed. Clarified task draft persistence/raw local input, UI policy preflight and historical narrow-width checks. No blocking findings. Browser/runtime/provider, current manual a11y/WCAG and human V3 acceptance were not performed; test links are not new runs. No changes to app code, DESIGN/assets, real profiles, hooks/trust, Git/publication or root site/.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG, owning RU/EN plan, registry/nav and product/architecture maps updated; EVALS/prod_test no_change_needed, existing rubrics and production history. Next DG05 by dependencies; DOCS-01–07 implemented, DOCS-13/16 in_progress until B, seven other tasks planned. Historical receipts below retain their original date and scope.

```text
python -B tools/check_docs.py
python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.docs_archive_checks.ProductAgentOsDocsArchiveTest.test_dg01_plan_translations_preserve_task_contracts -q
python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/documentation-architecture-2026-11-15.md
python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/documentation-architecture-2026-11-15.en.md
.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/dg04/site
tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/dg04/site
$env:PAOS_DOCS_SITE_DIR=(Resolve-Path .docs-tools/reports/dg04/site).Path
python -B -m unittest tests.product_agent_os.site_checks -q
python -B .docs-tools/reports/dg04/check_links.py
python -B .docs-tools/reports/dg04/check_source_links.py
git diff --check
```

## DG03 — implementation results {#dg03-results}

Historical DG03 receipt; current DG04 status is above.

Status: **completed / docs_static_verified**; DOCS-04/05/07 **implemented**. Date: 15-11-2026 16:46 Europe/Moscow. Original AC, Depends on, Blocks and feature task-state preserved.

| Task | Original AC coverage |
| --- | --- |
| DOCS-04 | AC1: modules/ownership/lifecycle, command/event/outbox, concurrency/idempotency/cancellation/recovery; AC2: real source/test links; AC3: Python plugin and Web service distinguished, F08 remains; AC4: metadata, 5 RU/EN pairs, nav/registry |
| DOCS-05 | AC1: 87 route families and 34 action-level rows covering request/response/auth/CSRF/errors/cursors/revisions/idempotency/side effects; AC2: handler/client/delegate/contracts/tests and synthetic examples; AC3: JSON polling is not SSE, no promised future Files/scan/DB; AC4: 4 RU/EN pairs, metadata/nav/registry |
| DOCS-07 | AC1: complete DDL for 16 objects (15 ordinary + FTS5), PK/FK/indexes/JSON, editable ERD; AC2: Worker/WAL/transactions/fences/import/snapshot/restore/search recovery without real DB access; AC3: PAOS SQLite separate from F33/M5; AC4: 7 DB RU/EN pairs and 1 atlas pair, metadata/nav/registry |

Current-run checks, receipts: .docs-tools/reports/dg03. Source check passed; source suite + translation-card regression 4/4; RU/EN matrices, 16 cards each, passed; strict isolated build and postprocess passed; site 7/7; affected HTML links/anchors passed; pinned source targets found for 34 pages. All 16 CREATE TABLE and 2 CREATE INDEX match source SQL after whitespace normalization. RU/EN endpoint inventories match. Local Chrome with disposable profile and Mermaid 10.9.6: ERD parse/render 2/2. git diff --check passed.

Review: self_review + separate_reused_context scoped API review by backend owner. Resolved insufficient action body detail, taskCreationApproved condition and two max-one ERD cardinalities; no blocking findings remain. Application tests are source references, not new runtime executions. Real DB, migrations, providers, human acceptance, publication and root site/ untouched.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG, RU/EN registry, product/architecture/atlas maps and navigation updated. EVALS/prod_test no_change_needed: rubrics and production history unchanged. Next group DG04; DOCS-08/09 also available by dependencies, not started automatically. DOCS-13/16 in_progress until B; eight other tasks planned.

```text
python -B tools/check_docs.py
python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.docs_archive_checks.ProductAgentOsDocsArchiveTest.test_dg01_plan_translations_preserve_task_contracts -q
python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/documentation-architecture-2026-11-15.md
python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/documentation-architecture-2026-11-15.en.md
.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/dg03/site
tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/dg03/site
$env:PAOS_DOCS_SITE_DIR=(Resolve-Path .docs-tools/reports/dg03/site).Path
python -B -m unittest tests.product_agent_os.site_checks -q
python -B .docs-tools/reports/dg03/check_links.py
python -B .docs-tools/reports/dg03/check_source_links.py
git diff --check
```

## DG02 — implementation results {#dg02-results}

Historical DG02 receipt; current DG03 status is above.

Status: **completed / docs_static_verified**; DOCS-01, DOCS-02, DOCS-03 **implemented**. Date: 15-11-2026 16:31 Europe/Moscow. Original AC, dependencies and feature task state preserved.

Created 13 full RU/EN pairs (26 pages): product/index and four product guides; architecture/index, system-context, containers, data-flow, decisions/index and two ADRs; one diagram in the existing atlas. Home, README, plugin entrypoints, navigation and registries route to current owners. Historical PRD/research retained, not presented as current runtime evidence.

| Card | Criteria met |
| --- | --- |
| DOCS-01 | AC1: purpose/owner/source/update matrix covers docs sections; AC2: three entrances and direct backend/frontend/DB/AI/planning routes in RU/EN; AC3: Web/local service, Python plugin and planned domains separate; AC4: metadata/source/test/limits and nav/registry synchronized |
| DOCS-02 | AC1: project/task/workflow/run/approval/evidence and invariants extracted with PRD provenance; AC2: source-present/historical/planned, F01–F34/M5 and README aligned; AC3: requirement→code/contract→test/evidence→owner; AC4: four complete RU/EN guides with metadata and limits |
| DOCS-03 | AC1: SPA/service/SQLite Worker thread/launcher/App/API/plugin linked to code; AC2: ADR rationale/alternatives/consequences and W03/W05→App-agent lineage retained without new owner acceptance; AC3: diagram only in atlas; AC4: RU/EN, sources/tests/limits and nav/registry aligned |

| Check | Command / result |
| --- | --- |
| Source docs | `python -B tools/check_docs.py`; `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — passed, 3/3 |
| Matrix and RU/EN cards | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <RU/EN documentation plan>`; `python -B -m unittest tests.product_agent_os.docs_archive_checks.ProductAgentOsDocsArchiveTest.test_dg01_plan_translations_preserve_task_contracts -q` — passed |
| Strict build | `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/dg02/site` — exit 0 |
| Language/site | `tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/dg02/site`; `PAOS_DOCS_SITE_DIR=.docs-tools/reports/dg02/site`, `python -B -m unittest tests.product_agent_os.site_checks -q` — 7/7 passed |
| HTML links/anchors | `python -B .docs-tools/reports/dg02/check_links.py` — missing targets/anchors: 0 |
| Mermaid | Installed Chrome, disposable profile, local Mermaid 10.9.6: parse + render both RU/EN diagrams, 2 SVGs, passed; no server/provider or disabled browser sandbox |
| Preservation/diff | Original IDs/AC/dependencies, historical research and feature JSON preserved; `git diff --check` passed |

Review: separate_reused_context (`dg02_review`) and self_review. Missing historical ADR-W05 finding resolved in RU/EN. Initial Chrome/Edge render attempts crashed in the sandbox (Edge AppContainer error); a reviewed launch of installed Chrome with process wait and a new profile rendered successfully. Failed receipts retained locally, not presented as diagram parse failures.

Control-plane sync: REQUIREMENTS/PLAN/RUNLOG, TEST evidence pointer, registry/nav and README updated; EVALS/prod_test no_change_needed because rubrics and historical production receipts did not change. AI quality, provider activation, actual app journeys, installation and publication not verified; application tests in guides are references, not new runs. DOCS-13/16 remain in_progress until B; the other 11 tasks are planned. Next independent branches: DG03 (backend/API/DB) and DG04 (frontend).

## DG01 — repair results {#dg01-results}

Historical DG01 receipt; subsequent DG02 status is recorded above.

Status: **completed / docs_static_verified**, 2026-11-15. **DOCS-13/A and DOCS-16/A completed**; parent DOCS-13/16 remain in_progress until B. DG02–DG07 and the other 14 tasks remain planned.

Eight full EN translations completed: UI V1/V2/V3, documentation architecture, functional remediation, audit remediation, ordinary route, Web task manager. Cards, statuses, dependencies, AC, dates, commands and historical limitations preserved. Semantic review and technical-literal comparison supplement the card/criteria completeness regression.

Repository-only file/directory links use verified blob/tree targets at commit 33ed0350738e549f932a9fffdeeff9d4908ca94c. EN JSON targets use the same snapshot; internal pages use relative links. Targets checked against the Git tree; snapshot available through the GitHub connector, not every external URL fetched individually. RU/EN project-formation anchors, language links and search/sitemap parity repaired.

The historical PostToolUse receipt retains five events; the current contract separately checks SessionStart/PreToolUse/PermissionRequest/Stop. Hooks/trust unchanged. The regression checks all cards, plain/backtick dependency IDs and AC numbering; group headings are separated from cards. Literal field names formatted in Russian prose without disabling the language gate.

| Check | Command / result |
| --- | --- |
| Matrices | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <plan>` — 16 RU/EN matrices passed |
| Source documentation | `python -B tools/check_docs.py`; `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — passed, 3/3 |
| Archive and translations | `python -B -m unittest tests.product_agent_os.docs_archive_checks -q` — 99/99 passed |
| Hook regression | Historical receipt / current hook shape / optional advisory targeted checks — 3/3 passed |
| Strict build | `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/dg01/site` — exit 0 |
| Language links | `tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/dg01/site` — passed |
| Site | `PAOS_DOCS_SITE_DIR=.docs-tools/reports/dg01/site`; `python -B -m unittest tests.product_agent_os.site_checks -q` — 7/7 passed |
| HTML links/anchors | `python -B .docs-tools/reports/dg01/check_links.py` — 30 affected RU/EN routes, missing targets/anchors: 0 |
| Diff | `git diff --check` — passed |

RED causes retained: original PostToolUse assertion, missing/partial translations, 17 EN JSON warnings, group/card boundary, literal field name, group Status and 7 directory/2 EN anchor targets. Corresponding GREEN checks followed repairs; earlier migration receipts below remain historical.

Review: self_review and independent translation/test review by agents with separate ownership; findings resolved. Control-plane sync: PLAN/RUNLOG, catalog and RU/EN registries updated; TEST contains an evidence pointer. REQUIREMENTS/EVALS/prod_test no_change_needed: scope, rubrics and production history unchanged. Feature JSON task state/dependencies preserved. Root site/, publication, runtime/provider activation and future domain docs are outside the result. Next planned stage: DG02.

## Migration evidence and checks

Historical migration status: relocation and backlog recorded; partially verified, site publication not ready at that point. Product tasks were not implemented.

- Preservation: 42/42 original files matched path/link relocation and addition of missing Source status only. Literal template examples were retained; seven JSON owners preserved task IDs/status/dependencies/AC/receipts. Old files were absent and 42 new owners existed.
- Task matrices: new DOCS and current FUNC/Web/audit/ordinary-route passed validate_task_matrix; DOCS DAG 16/16 was acyclic.
- Source/docs and path-dependent tests: 120 tests passed (5.614s); check_docs exit0. Three affected fixture helpers passed: graph/backend gates, hygiene docs loading and doubt artifact path.
- Archive: 98 tests, six failures. Five assertions identified eight missing EN sibling pages after research/design plans and the new backlog entered docs. One required PostToolUse absent already in baseline hooks.json; the hook was not changed or enabled for the test.
- Strict MkDocs baseline from HEAD: exit1, 42 WARNING lines (21 RU + 21 EN); migration preview: exit1, 351 WARNING lines (330 RU + 21 EN). The final line reports only the last language's 21 warnings; the initial tail-based estimate was incomplete and corrected after the whole log was read. New RU warnings arose from relocated research/design plans and the new backlog linking to code/evidence outside docs, and direct EN sibling links in the catalog. Repository targets existed, but were not published-site links. Publication needed DOCS-16; root site was not replaced.
- Site checks after the existing fix_site_i18n_links step: seven tests, four failures involving missing EN pages and search/source parity; a failed strict build was not concealed.
- Fixed intermediate errors: template angle-link rebasing, CRLF insertion boundaries, extra JSON backlinks, legacy DOCS-relative inventories and expected-path sorting. Assertions were not disabled; no formal EN placeholders were added.

Commands: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_coding_standards_artifacts tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_validators tests.product_agent_os.test_doubt_verification -q`; `python -B tools/check_docs.py`; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py` for each of the five named plans; `python -B -m unittest tests.product_agent_os.docs_archive_checks -q`; `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/planning-relocation-2026-11-15/site`; `tools/fix_site_i18n_links.ps1 -SiteDir .docs-tools/reports/planning-relocation-2026-11-15/site`; `python -B -m unittest tests.product_agent_os.site_checks -q` with PAOS_DOCS_SITE_DIR pointing to that preview; `git diff --check`. Local raw logs: .docs-tools/reports/planning-relocation-2026-11-15/ (not published).

DOCS-16/A and DOCS-13/A belong to mandatory first group DG01; DOCS-16/B and DOCS-13/B retain original full-closure dependencies. The historical PostToolUse check is compared with the current contract without changing trust for green tests. EVALS/prod_test received mechanical references only, without changing rubrics or historical verdicts; TEST routing was retained.

The eight EN gaps identified by that migration were: 2026-11-13-ui-implementation-plan.md, 2026-11-13-v2-ui-implementation-plan.md, 2026-11-13-v3-ui-implementation-plan.md, documentation-architecture-2026-11-15.md, functional-remediation-2026-11-15.md, product-agent-os-audit-remediation-task-plan-2026-11-09.md, product-agent-os-ordinary-route-implementation-plan-2026-11-05.md and product-agent-os-web-task-manager-plan-2026-11-09.md, all in docs/planning. They represented real translation debt, not full RU/EN parity.

## Separate task list

There are 16 documentation tasks: DOCS-01–07 implemented, DOCS-13/16 in_progress until B, other 7 planned. This does not change FUNC/M5 status.

| ID | Task / directory | Deliverables | Dependencies |
| --- | --- | --- | --- |
| PAOS-DOCS-01 | Separate implementation documentation, user guides and the knowledge base — `docs/index.md + docs/product/index.md` | Section map with three entry points: developing PAOS, using PAOS, and Codex/methodology knowledge. | none |
| PAOS-DOCS-02 | Assemble the current product specification and domain model — `docs/product/` | overview.md, domain-model.md, capabilities.md, user-journeys.md. | `PAOS-DOCS-01` |
| PAOS-DOCS-03 | Consolidate the architecture and decision log — `docs/architecture/ and docs/architecture/decisions/` | system-context.md, containers.md, data-flow.md, decisions/index.md. | `PAOS-DOCS-01`, `PAOS-DOCS-02` |
| PAOS-DOCS-04 | Document the backend and local-service lifecycle — `docs/backend/` | index.md, modules.md, lifecycle.md, commands-events.md, recovery.md. | `PAOS-DOCS-03` |
| PAOS-DOCS-05 | Create the HTTP API, event and shared-contract reference — `docs/api/` | index.md, endpoints.md, events.md, errors.md; OpenAPI only after deciding on a supported generator. | `PAOS-DOCS-03`, `PAOS-DOCS-04` |
| PAOS-DOCS-06 | Document the frontend, UI/UX and navigation states — `docs/frontend/` | index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md. | `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03` |
| PAOS-DOCS-07 | Document the actual SQLite schema and data lifecycle — `docs/db/` | index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md. | `PAOS-DOCS-03`, `PAOS-DOCS-05` |
| PAOS-DOCS-08 | Document PAOS AI orchestration and agent operation — `docs/ai/ and docs/ai/agents/` | index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md. | `PAOS-DOCS-03`, `PAOS-DOCS-05` |
| PAOS-DOCS-09 | Document LLM routes, prompts and model/provider boundaries — `docs/ai/llm/` | index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md. | `PAOS-DOCS-08` |
| PAOS-DOCS-10 | Document search, retrieval and RAG boundaries — `docs/ai/rag/` | index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md. | `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09` |
| PAOS-DOCS-11 | Align discovery and project-graph documentation — `docs/code-intelligence/` | index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md. | `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-10` |
| PAOS-DOCS-12 | Assemble product security/privacy and trust-boundary documentation — `docs/security/` | index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md. | `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-07`, `PAOS-DOCS-08` |
| PAOS-DOCS-13 | Create a map of tests, evals and evidence boundaries — `docs/testing/` | index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md. | `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08` |
| PAOS-DOCS-14 | Document local operations, packaging and recovery — `docs/operations/` | index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md. | `PAOS-DOCS-04`, `PAOS-DOCS-07`, `PAOS-DOCS-12`, `PAOS-DOCS-13` |
| PAOS-DOCS-15 | Organize Python plugin, skills and learning-loop documentation — `docs/product-agent-os/ (existing section)` | Current index, module map, CLI/contracts cross-links and separation of staged/manual_only/active. | `PAOS-DOCS-01`, `PAOS-DOCS-03`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-13` |
| PAOS-DOCS-16 | Connect documentation tasks to feature delivery and verify navigation — `docs/planning/ + mkdocs.yml + docs/sources/` | Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes. | `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03`, `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09`, `PAOS-DOCS-10`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-15` |

### Task `PAOS-DOCS-01`

- Task: PAOS-DOCS-01 — Separate implementation documentation, user guides and the knowledge base
- Status: implemented
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:31
- Priority: P1
- Depends on: none
- Blocks: `PAOS-DOCS-02`, `PAOS-DOCS-03`, `PAOS-DOCS-06`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [docs/index.md](../index.md), [docs/product-agent-os/index.md](../product-agent-os/index.md), [docs/agent-systems/overview.md](../agent-systems/overview.md), [docs/methodologies/index.md](../methodologies/index.md)
- Short description: Separate implementation documentation, user guides and the knowledge base
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/index.md + docs/product/index.md; restructure; Section map with three entry points: developing PAOS, using PAOS, and Codex/methodology knowledge.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: Section map with three entry points: developing PAOS, using PAOS, and Codex/methodology knowledge.
- Acceptance criteria: AC1: Every section has a purpose, owner, source of truth and update rules; no empty categories are created merely for their names. AC2: RU/EN navigation makes backend/frontend/DB/AI and current plans discoverable without reading the historical RUNLOG. AC3: Current Web/desktop, the Python plugin and future features are identified separately; a folder name does not imply implementation completeness. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: Section map with three entry points: developing PAOS, using PAOS, and Codex/methodology knowledge. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All four original criteria completed in DG02; details mapped in the group results.
- files touched / work locations: docs/index*, docs/product/index*, mkdocs.yml, README.md
- technical value delivered: Canonical ownership and source/contract/test/task traceability; docs_static_verified.
- product value delivered: Current capabilities, boundaries and next steps are discoverable in both languages.
- actual implementation date and time: 15-11-2026 16:31
- verification evidence: [DG02 checks and AC mapping](#dg02-results).
- residual risks: Source drift; no new application runtime/provider/human acceptance.
- follow-up: DG03/DG04 subject to original dependencies; update the canonical page when its contract changes.
- Documentation impact: RU/EN, navigation, registry and owning control-plane pointers synchronized.

### Task `PAOS-DOCS-02`

- Task: PAOS-DOCS-02 — Assemble the current product specification and domain model
- Status: implemented
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:31
- Priority: P2
- Depends on: `PAOS-DOCS-01`
- Blocks: `PAOS-DOCS-03`, `PAOS-DOCS-06`, `PAOS-DOCS-16`
- Source: [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md](product-agent-os-web-task-manager-plan-2026-11-09.md), [REQUIREMENTS.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/REQUIREMENTS.md), [packages/contracts/issues/task-profile.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/issues/task-profile.ts)
- Short description: Assemble the current product specification and domain model
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/product/; extract_and_move; overview.md, domain-model.md, capabilities.md, user-journeys.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: overview.md, domain-model.md, capabilities.md, user-journeys.md.
- Acceptance criteria: AC1: Extract current project/task/workflow/run/approval/evidence entities, invariants and user journeys from the PRD; preserve earlier versions with provenance. AC2: Current/implemented-not-verified/planned and F01–F34/M5 are linked to task owners; README and source-backed claims do not contradict them. AC3: Trace requirement → code/contract → test/evidence → owning task; do not create independently maintained duplicate requirements. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: overview.md, domain-model.md, capabilities.md, user-journeys.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All four original criteria completed in DG02; details mapped in the group results.
- files touched / work locations: docs/product/{overview,domain-model,capabilities,user-journeys}.{md,en.md}
- technical value delivered: Canonical ownership and source/contract/test/task traceability; docs_static_verified.
- product value delivered: Current capabilities, boundaries and next steps are discoverable in both languages.
- actual implementation date and time: 15-11-2026 16:31
- verification evidence: [DG02 checks and AC mapping](#dg02-results).
- residual risks: Source drift; no new application runtime/provider/human acceptance.
- follow-up: DG03/DG04 subject to original dependencies; update the canonical page when its contract changes.
- Documentation impact: RU/EN, navigation, registry and owning control-plane pointers synchronized.

### Task `PAOS-DOCS-03`

- Task: PAOS-DOCS-03 — Consolidate the architecture and decision log
- Status: implemented
- Delivery group: DG02
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:31
- Priority: P1
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`
- Blocks: `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [research/product-agent-os-web-architecture-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-architecture-2026-11-05.md), [research/batch45-professional-code-authoring-architecture-v2.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/batch45-professional-code-authoring-architecture-v2.md), [research/batch45-professional-code-authoring-solution-map.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/batch45-professional-code-authoring-solution-map.md), [docs/product-agent-os/architecture.md](../product-agent-os/architecture.md), [docs/diagrams/index.md](../diagrams/index.md)
- Short description: Consolidate the architecture and decision log
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/architecture/ and docs/architecture/decisions/; extract_and_move; system-context.md, containers.md, data-flow.md, decisions/index.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: system-context.md, containers.md, data-flow.md, decisions/index.md.
- Acceptance criteria: AC1: Map Web SPA, local service, SQLite worker, launcher/desktop, Codex App/API routes and the Python plugin to actual source files. AC2: Extract historical proposals without promoting their status; ADRs include status, rationale, alternatives and consequences. AC3: Keep diagrams in the existing atlas and link them to architecture; do not create a conflicting second model. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: system-context.md, containers.md, data-flow.md, decisions/index.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All four original criteria completed in DG02; details mapped in the group results.
- files touched / work locations: docs/architecture/, docs/diagrams/paos-application-architecture.{md,en.md}
- technical value delivered: Canonical ownership and source/contract/test/task traceability; docs_static_verified.
- product value delivered: Current capabilities, boundaries and next steps are discoverable in both languages.
- actual implementation date and time: 15-11-2026 16:31
- verification evidence: [DG02 checks and AC mapping](#dg02-results).
- residual risks: Source drift; no new application runtime/provider/human acceptance.
- follow-up: DG03/DG04 subject to original dependencies; update the canonical page when its contract changes.
- Documentation impact: RU/EN, navigation, registry and owning control-plane pointers synchronized.

### Task `PAOS-DOCS-04`

- Task: PAOS-DOCS-04 — Document the backend and local-service lifecycle
- Status: implemented
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:46
- Priority: P1
- Depends on: `PAOS-DOCS-03`
- Blocks: `PAOS-DOCS-05`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts), [apps/local-service/src/execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/execution-recipes/service.mts), [apps/local-service/src/supervisor](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/supervisor), [research/product-agent-os-web-m2c-execution-2026-11-12.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m2c-execution-2026-11-12.md)
- Short description: Document the backend and local-service lifecycle
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/backend/; write_from_source; index.md, modules.md, lifecycle.md, commands-events.md, recovery.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, modules.md, lifecycle.md, commands-events.md, recovery.md.
- Acceptance criteria: AC1: Document modules and ownership, command/event/outbox flow, concurrency, idempotency, errors, cancellation and shutdown/recovery. AC2: Provide actual entrypoints/contracts and tests, rather than an abstract backend description from methodologies/backend.md. AC3: Distinguish Web runtime from the Python plugin; describe current cross-layer dependencies honestly with a reference to F08, without claiming they have already been repaired. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, modules.md, lifecycle.md, commands-events.md, recovery.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All original AC completed; see DG03 coverage table.
- files touched / work locations: docs/backend/ RU/EN
- technical value delivered: source-grounded canonical contracts and verification traceability
- product value delivered: Current behavior, limits and change paths documented.
- actual implementation date and time: 15-11-2026 16:46
- verification evidence: [DG03](#dg03-results)
- residual risks: source drift; no new runtime/provider/human acceptance
- follow-up: DG04; other groups follow original dependencies
- Documentation impact: canonical RU/EN guides, navigation, registry and owning control-plane updated

### Task `PAOS-DOCS-05`

- Task: PAOS-DOCS-05 — Create the HTTP API, event and shared-contract reference
- Status: implemented
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:46
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-04`
- Blocks: `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/http/session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/session-gate.mts), [apps/web/src/api/client.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/api/client.ts), [packages/contracts](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts)
- Short description: Create the HTTP API, event and shared-contract reference
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/api/; write_from_source; index.md, endpoints.md, events.md, errors.md; OpenAPI only after deciding on a supported generator.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, endpoints.md, events.md, errors.md; OpenAPI only after deciding on a supported generator.
- Acceptance criteria: AC1: List request/response, auth/CSRF, errors, pagination, revision/cursor, idempotency and side effects for current routes. AC2: Fixtures/examples are synthetic; cross-check the endpoint inventory against handlers/clients/tests and explicitly mark unsupported capabilities. AC3: The contract does not promise missing Files/scan/DB endpoints F26–F34; schema generation does not run target scripts. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, endpoints.md, events.md, errors.md; OpenAPI only after deciding on a supported generator. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All original AC completed; see DG03 coverage table.
- files touched / work locations: docs/api/ RU/EN
- technical value delivered: source-grounded canonical contracts and verification traceability
- product value delivered: Current behavior, limits and change paths documented.
- actual implementation date and time: 15-11-2026 16:46
- verification evidence: [DG03](#dg03-results)
- residual risks: source drift; no new runtime/provider/human acceptance
- follow-up: DG04; other groups follow original dependencies
- Documentation impact: canonical RU/EN guides, navigation, registry and owning control-plane updated

### Task `PAOS-DOCS-06`

- Task: PAOS-DOCS-06 — Document the frontend, UI/UX and navigation states
- Status: implemented
- Delivery group: DG04
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:57
- Priority: P1
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03`
- Blocks: `PAOS-DOCS-13`, `PAOS-DOCS-16`
- Source: [DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/DESIGN.md), [design/2026-11-13-v3/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/README.md), [design/2026-11-13-v3/task-field-map.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/task-field-map.md), [apps/web/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/README.md), [apps/web/src/ui/App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/App.tsx), [apps/web/src/features](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features), [docs/web/accessibility.md](../web/accessibility.md)
- Short description: Document the frontend, UI/UX and navigation states
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/frontend/; extract_and_write; index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md.
- Acceptance criteria: AC1: Describe existing screens/routes/components, API state, drafts, polling/late responses, themes and RU/EN with code references. AC2: DESIGN and visual assets retain design ownership; docs/frontend provides a usage map, not another copy of tokens/screenshots. AC3: Mark future Files/Map/Database/usages from F26–F34 planned; distinguish current accessibility evidence from human/WCAG gaps. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, navigation.md, state-management.md, components.md, design-system.md, accessibility.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Maintain the canonical guide with source changes; DG05 follows dependencies.

#### Completion Report

- status: implemented
- what was done: All four original AC completed; see DG04 coverage.
- files touched / work locations: docs/frontend/ six RU/EN pairs; nav/registry/maps/control-plane
- technical value delivered: source-grounded screen/component/state and design ownership map
- product value delivered: Current behavior, draft preservation, limits and future capabilities clearly distinguished.
- actual implementation date and time: 15-11-2026 16:57
- verification evidence: [DG04](#dg04-results)
- residual risks: source drift; historical browser evidence; no new human/WCAG acceptance
- follow-up: DG05 by original dependencies
- Documentation impact: canonical RU/EN guides, nav, registry, plan and control-plane updated

### Task `PAOS-DOCS-07`

- Task: PAOS-DOCS-07 — Document the actual SQLite schema and data lifecycle
- Status: implemented
- Delivery group: DG03
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 16:46
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`
- Blocks: `PAOS-DOCS-10`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/storage/migrations/schema.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/migrations/schema.mts), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts), [apps/local-service/src/storage/local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/local-store.mts), [apps/local-service/src/storage/restore-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/restore-worker.mts), [research/product-agent-os-web-storage-research-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-storage-research-2026-11-09.md)
- Short description: Document the actual SQLite schema and data lifecycle
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/db/; extract_and_write; index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md.
- Acceptance criteria: AC1: Cross-check tables/columns/PK/FK/indexes/FTS, JSON payloads and schema/checksum/version fences against source; provide an editable Mermaid ERD and explain authority. AC2: Link WAL/worker ownership, transactions/idempotency, snapshot/backup/restore/import and failure cases to tests; do not open the user's real databases. AC3: Distinguish PAOS SQLite from the target project database F33; mark PostgreSQL/pgvector M5 planned rather than current storage. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, schema.md, erd.md, migrations.md, transactions.md, backup-restore.md, search-index.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: implemented
- what was done: All original AC completed; see DG03 coverage table.
- files touched / work locations: docs/db/ RU/EN, docs/diagrams/paos-sqlite-erd.md and .en.md
- technical value delivered: source-grounded canonical contracts and verification traceability
- product value delivered: Current behavior, limits and change paths documented.
- actual implementation date and time: 15-11-2026 16:46
- verification evidence: [DG03](#dg03-results)
- residual risks: source drift; no new runtime/provider/human acceptance
- follow-up: DG04; other groups follow original dependencies
- Documentation impact: canonical RU/EN guides, navigation, registry and owning control-plane updated

### Task `PAOS-DOCS-08`

- Task: PAOS-DOCS-08 — Document PAOS AI orchestration and agent operation
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`
- Blocks: `PAOS-DOCS-09`, `PAOS-DOCS-10`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts), [apps/local-service/src/runtime/app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-gateway.mts), [apps/local-service/src/runtime/codex/coordinator.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/codex/coordinator.ts), [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts), [docs/product-agent-os/live-runtime-governance.md](../product-agent-os/live-runtime-governance.md), [docs/agent-systems/subagents-skills.md](../agent-systems/subagents-skills.md)
- Short description: Document PAOS AI orchestration and agent operation
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/ai/ and docs/ai/agents/; extract_and_write; index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md.
- Acceptance criteria: AC1: Describe the actual dispatch/attach/session/approval/Stop flow and the division of responsibility between Codex and PAOS; do not conflate configured/pinned/observed status. AC2: Show Web execution and packaged lifecycle agents/skills as separate surfaces with actual selectors/callers. AC3: General agent-systems advice remains reference material; every implementation description links to code and evidence without promising autonomous hosted delivery. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, agents/orchestration.md, agents/context.md, agents/tools-approvals.md, agents/sessions.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-09`

- Task: PAOS-DOCS-09 — Document LLM routes, prompts and model/provider boundaries
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-10`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/runtime/route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/route-selector.ts), [apps/local-service/src/connections](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/connections), [research/product-agent-os-web-auth-commercial-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-auth-commercial-2026-11-09.md), [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py)
- Short description: Document LLM routes, prompts and model/provider boundaries
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/ai/llm/; extract_and_write; index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md.
- Acceptance criteria: AC1: Document codex_app_agent and local_api_byok, explicit route choice/no silent fallback, credentials and failure recovery from source; recheck external OpenAI claims against official sources when writing. AC2: Inventory prompt/output contracts and owners; do not describe a deterministic proposal gate as live LLM generation. AC3: Limit tokens/cost/latency claims to observable sources; mark F11/F15 and missing capabilities planned/unknown and keep secrets out of examples. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, routes.md, prompts-and-outputs.md, budgets-and-observability.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-10`

- Task: PAOS-DOCS-10 — Document search, retrieval and RAG boundaries
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09`
- Blocks: `PAOS-DOCS-11`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/storage/search-queries.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/search-queries.mts), [plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_chunking.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_semantic.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_embedding_provider.py), [plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/project_graph_hybrid_retrieval.py), [docs/product-agent-os/project-code-graph.md](../product-agent-os/project-code-graph.md)
- Short description: Document search, retrieval and RAG boundaries
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/ai/rag/; extract_and_write; index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md.
- Acceptance criteria: AC1: Describe Web SQLite FTS5, Python graph retrieval/semantic cache and approval-bound provider adapters separately; explicitly state the lack of confirmed end-to-end Web RAG. AC2: For existing paths record corpus/filters/chunking/revision/freshness, query budget and failure/rollback; do not imply live embeddings. AC3: Distinguish retrieval quality from answer quality; current deterministic checks, future provider evals and M5 pgvector have different statuses. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, corpus-and-indexing.md, retrieval.md, freshness-and-provenance.md, evaluation.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-11`

- Task: PAOS-DOCS-11 — Align discovery and project-graph documentation
- Status: planned
- Delivery group: DG05
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-10`
- Blocks: `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/code-index/lexical.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/lexical.mts), [plugins/product-agent-os/scripts/product_agent_os/discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py), [plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py), [docs/product-agent-os/project-code-graph.md](../product-agent-os/project-code-graph.md), [docs/product-agent-os/graph-intelligence-contract.md](../product-agent-os/graph-intelligence-contract.md)
- Short description: Align discovery and project-graph documentation
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/code-intelligence/; reuse_and_write; index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md.
- Acceptance criteria: AC1: Describe Python core discovery/graph and the Web lexical graph separately, with a language/relation/source/limits matrix and actual integration status. AC2: Existing graph-contract sources retain ownership; navigation links explain which path Web uses and which CLI uses. AC3: Mark F26–F34 and PoC engines planned until runtime evidence exists; the feature owner updates docs when implementing the corresponding FUNC task. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, discovery.md, inventory.md, graph-model.md, queries-impact.md, adapters.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-12`

- Task: PAOS-DOCS-12 — Assemble product security/privacy and trust-boundary documentation
- Status: planned
- Delivery group: DG06
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Depends on: `PAOS-DOCS-03`, `PAOS-DOCS-05`, `PAOS-DOCS-07`, `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-14`, `PAOS-DOCS-16`
- Source: [apps/local-service/src/http/session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/session-gate.mts), [apps/local-service/src/runtime/app-agent-files.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-files.mts), [apps/local-service/src/redaction](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/redaction), [docs/product-agent-os/privacy-supply-chain-retention.md](../product-agent-os/privacy-supply-chain-retention.md), [research/product-agent-os-web-auth-commercial-2026-11-09.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-auth-commercial-2026-11-09.md)
- Short description: Assemble product security/privacy and trust-boundary documentation
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/security/; extract_and_write; index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md.
- Acceptance criteria: AC1: Link local HTTP/session/CSRF/origin, filesystem root, approvals, credentials, redaction and profile isolation to guards/tests. AC2: Distinguish platform guidance in codex/security.md from actual application limitations; configured policy is not proven enforcement. AC3: Include no secrets/PII/real profile dumps; preserve commercial/license gaps and external authority gates. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, threat-model.md, filesystem.md, auth-credentials.md, data-retention.md, supply-chain.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-13`

- Task: PAOS-DOCS-13 — Create a map of tests, evals and evidence boundaries
- Status: in_progress
- Delivery group: DG01 (A), DG06 (B; full closure)
- Execution stages: A — DG01, without future domain prerequisites; B — after A and all original Depends on. Completing A does not close the task; full scope/AC are preserved. Stage A completed; B planned.
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`
- Blocks: `PAOS-DOCS-14`, `PAOS-DOCS-15`, `PAOS-DOCS-16`
- Source: [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md), [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/EVALS.md), [tests/web](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/web), [tests/product_agent_os](https://github.com/alexroadcaster/product-agent-os/tree/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/product_agent_os), [docs/product-agent-os/behavioral-evals.md](../product-agent-os/behavioral-evals.md), [docs/web/accessibility.md](../web/accessibility.md)
- Short description: Create a map of tests, evals and evidence boundaries
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/testing/; extract_and_write; index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md.
- Acceptance criteria: AC1: Link every subsystem to targeted test/eval/browser/native checks and escalation conditions; TEST/EVALS remain operational owners of commands/thresholds. AC2: Do not conflate historical receipts, current checks, human acceptance or production claims; make flaky/blocked scenarios visible. AC3: Establish a verifiable source links → strict preview → RU/EN/search/site parity route; distinguish current migration failures from baseline and do not weaken checks. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, test-map.md, synthetic-vs-live.md, ai-evals.md, documentation-checks.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: in_progress
- what was done: Stage A completed in DG01; stage B and full parent acceptance remain open.
- files touched / work locations: docs/planning/, affected guides/registries and docs_archive_checks.py; isolated .docs-tools/reports/dg01/site.
- technical value delivered: Stage A docs_static_verified; B not_implemented.
- product value delivered: Working RU/EN navigation and preserved planning contracts; future subsystem guides remain planned.
- actual implementation date and time: Stage A 15-11-2026; full task pending_execution_timestamp.
- verification evidence: [DG01 results](#dg01-results); archive 99/99, source 3/3, site 7/7; matrices, strict build and HTML links passed.
- residual risks: Stage B dependencies and original full-task AC remain mandatory.
- follow-up: DG06 / DOCS-13/B after original dependencies; next branches DG03/DG04.
- Documentation impact: Stage A synchronized with owning plan, catalog, registries and control plane; domain documentation remains planned.

### Task `PAOS-DOCS-14`

- Task: PAOS-DOCS-14 — Document local operations, packaging and recovery
- Status: planned
- Delivery group: DG07
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-04`, `PAOS-DOCS-07`, `PAOS-DOCS-12`, `PAOS-DOCS-13`
- Blocks: `PAOS-DOCS-16`
- Source: [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md), [apps/desktop-local/distribution.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/distribution.mts), [apps/launcher/launcher.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/launcher/launcher.ts), [docs/web/pilot.md](../web/pilot.md), [docs/release/web-m4-local-release.json](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/release/web-m4-local-release.json), [research/product-agent-os-web-m4-0030-execution-2026-11-12.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m4-0030-execution-2026-11-12.md)
- Short description: Document local operations, packaging and recovery
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/operations/; extract_and_write; index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md.
- Acceptance criteria: AC1: Cross-check commands and parameters against CLI/launcher; make paths/profile ownership and normal Stop clear; do not present hazardous actions as default troubleshooting. AC2: Separate build/package/qualification/install/upgrade/rollback; moving receipts does not remove unsigned/local/human/commercial gaps. AC3: F17 remains a separate implementation task; documentation does not publish or install the application. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: index.md, install-start-stop.md, profiles.md, upgrade-rollback.md, troubleshooting.md, release-boundaries.md. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-15`

- Task: PAOS-DOCS-15 — Organize Python plugin, skills and learning-loop documentation
- Status: planned
- Delivery group: DG07
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-03`, `PAOS-DOCS-08`, `PAOS-DOCS-11`, `PAOS-DOCS-13`
- Blocks: `PAOS-DOCS-16`
- Source: [plugins/product-agent-os/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/README.md), [docs/product-agent-os/cli-reference.md](../product-agent-os/cli-reference.md), [docs/product-agent-os/project-formation.md](../product-agent-os/project-formation.md), [docs/product-agent-os/self-learning-loop.md](../product-agent-os/self-learning-loop.md), [plugins/product-agent-os/scripts/product_agent_os/self_learning_state.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/self_learning_state.py)
- Short description: Organize Python plugin, skills and learning-loop documentation
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/product-agent-os/ (existing section); reuse_and_reorganize; Current index, module map, CLI/contracts cross-links and separation of staged/manual_only/active.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: Current index, module map, CLI/contracts cross-links and separation of staged/manual_only/active.
- Acceptance criteria: AC1: Reuse existing substantive plugin guides and add missing module/consumer links; do not create a duplicate plugin directory. AC2: Agents/skills/hooks/templates/validators/learning candidates have current owners and update rules; file presence does not prove activation. AC3: Preserve manual-only/candidate-only and target-preservation contracts; separate task history from guides. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: Current index, module map, CLI/contracts cross-links and separation of staged/manual_only/active. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: planned
- what was done: scope and acceptance defined; subsystem documentation has not yet been written.
- files touched / work locations: the future directory is specified in Scope.
- technical value delivered: not_implemented
- product value delivered: not_verified
- actual implementation date and time: pending_execution_timestamp
- verification evidence: static source comparison; future checks have not been executed.
- residual risks: source drift and conflating historical/planned/current states and UI/plugin/runtime surfaces.
- follow-up: select a bounded slice according to dependencies.
- Documentation impact: the future source-owned section, registry/nav and only affected control-plane owners.

### Task `PAOS-DOCS-16`

- Task: PAOS-DOCS-16 — Connect documentation tasks to feature delivery and verify navigation
- Status: in_progress
- Delivery group: DG01 (A), DG07 (B; full closure)
- Execution stages: A — DG01, without future domain prerequisites; B — after A and all original Depends on. Completing A does not close the task; full scope/AC are preserved. Stage A completed; B planned.
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: owner requested implementation documentation audit and separate backlog
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Depends on: `PAOS-DOCS-01`, `PAOS-DOCS-02`, `PAOS-DOCS-03`, `PAOS-DOCS-04`, `PAOS-DOCS-05`, `PAOS-DOCS-06`, `PAOS-DOCS-07`, `PAOS-DOCS-08`, `PAOS-DOCS-09`, `PAOS-DOCS-10`, `PAOS-DOCS-11`, `PAOS-DOCS-12`, `PAOS-DOCS-13`, `PAOS-DOCS-14`, `PAOS-DOCS-15`
- Blocks: none
- Source: [docs/planning/functional-remediation-2026-11-15.json](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/functional-remediation-2026-11-15.json), [docs/planning/functional-remediation-2026-11-15.md](functional-remediation-2026-11-15.md), [mkdocs.yml](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/mkdocs.yml), [docs/sources/registry.md](../sources/registry.md), [docs/sources/registry.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/sources/registry.en.md)
- Short description: Connect documentation tasks to feature delivery and verify navigation
- Technical value: Canonical ownership, source-to-contract traceability and a lower risk of incorrect agent code changes.
- Product value: Developers and users understand current behavior, limitations and the next step.
- Scope: docs/planning/ + mkdocs.yml + docs/sources/; integrate_and_verify; Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes.
- Non-goals: New functionality, silent provider/runtime activation, rewriting evidence or duplicating methodologies.
- Expected result: Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes.
- Acceptance criteria: AC1: Every FUNC delivery group has a documentation owner and affected-section list; feature closure updates its own changed facts, not the entire knowledge base. AC2: Check links/anchors, localization and search/sitemap on an isolated strict build; route old addresses or explicitly document migration and preserve historical receipts. AC3: All 16 documentation tasks have source/acceptance/status; this planning task does not start CI/automation/publication. AC5: Resolve the eight EN gaps listed in evidence with substantive translations; strict build and site checks pass and no new migration warnings remain. AC4: Include Source status, owner, scope/version, source links, related tests and known limitations; update related RU/EN/nav/registry without false implemented/live claims.
- Verification gates: Source/code cross-check, Markdown links, scoped check_docs, task matrix validator; strict isolated MkDocs and affected site checks for nav/render; record exact commands/results during execution.
- Risks / approval gates: Do not present a plan as implementation. Live/provider/user profile/installation/publication actions are not authorized; recheck stale sources before writing.
- Complexity: medium; broad source reconciliation; exact scope follows current-source review
- Estimated execution time: Not estimated: first bound the source/module slice; timing is not a commitment.
- Agents: docs-maintainer with the source owner; proposed roles, no team launched by this planning card
- Skills: documentation-and-adrs; implementation-specific skills only when needed
- Output artifacts: Owner/update matrix, RU/EN navigation, redirect/link map, maintained current-state indexes. This card owns status and receipts; RUNLOG owns the concise handoff.
- Rollback: Only owned changes, preserving source history, backlink map and earlier documents.
- Next step: Check dependencies and select one documentation slice; do not start the entire backlog automatically.

#### Completion Report

- status: in_progress
- what was done: Stage A completed in DG01; stage B and full parent acceptance remain open.
- files touched / work locations: docs/planning/, affected guides/registries and docs_archive_checks.py; isolated .docs-tools/reports/dg01/site.
- technical value delivered: Stage A docs_static_verified; B not_implemented.
- product value delivered: Working RU/EN navigation and preserved planning contracts; future subsystem guides remain planned.
- actual implementation date and time: Stage A 15-11-2026; full task pending_execution_timestamp.
- verification evidence: [DG01 results](#dg01-results); archive 99/99, source 3/3, site 7/7; matrices, strict build and HTML links passed.
- residual risks: Stage B dependencies and original full-task AC remain mandatory.
- follow-up: DG07 / DOCS-16/B after original dependencies; next branches DG03/DG04.
- Documentation impact: Stage A synchronized with owning plan, catalog, registries and control plane; domain documentation remains planned.
