# Product-Agent OS — direction B: methodologies for user projects

Source status: repository_source / owner_requested_plan / B1_B2_B3_B4_locally_verified; release_hold.
Created: 2026-11-15. Revised: 2026-11-19. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Purpose and two independent directions

**A — Product-Agent OS internal quality:** [internal plan](methodology-improvement-2026-11-15.en.md), [JSON](methodology-improvement-2026-11-15.json): 17 executable tasks with existing IDs retained; METH-16 is retained separately as a reference-only record.

**B — this product plan:** 26 PAOS-PMETH-01–26 tasks extend selection, application and verification of Spec-Driven Development (Spec-DD), Design-Driven Development (Design-DD), Test-Driven Development (TDD), Agentic-Driven Development (ADD) and Feature-Sliced Design (FSD) in user projects. [JSON](user-project-methodologies-2026-11-15.json) owns status/priority/dependencies; [Russian](user-project-methodologies-2026-11-15.md) contains matching detailed cards.

B does not depend on A's internal dashboard/tasks/workflows FSD migration, METH-18 go decisions or completion of all FUNC groups. Shared files require coordinated ownership/sequential writes rather than invented functional dependencies. The owner authorized B1 for local source changes and synthetic verification. Remaining groups retain their own start criteria.

## Existing implementation and remaining evidence

Source snapshot: git HEAD `5a9c87bea374accc953a8401fa1ac32678ff6e6e`; JSON records 15 source-owner hashes. This is source inspection, not a new runtime/model/browser acceptance run. The initial FUNC owner snapshot had 10 implemented / 24 planned after G01/G02. Concurrent FUNC-G03 started during planning; its live task-state and later source edits belong to that workstream and are not frozen by this matrix. These are not fresh runtime receipts; future slices require current source reads.

The 2026-11-18 review of the current FUNC owner recorded 33 implemented and F23 awaiting_user_decision. Reuse F02 (task/artifact links), F13 (document apply), F14 (code index) and F27–29 (project analysis and source links). These are FUNC matrix statuses. This review did not rerun the runtime. The review records primary sources and Context7 findings and limitations checked on 2026-11-18.

| Area | Source observation | New task responsibility |
| --- | --- | --- |
| Discovery/intake | discovery.py calls build_methodology_audit; task_routing.py has explicit context and file-free intake | PMETH-01/02 verify the path and retain intent/provenance without another scanner |
| Catalog/audit/synthesis | Twelve domains, recommendations, readiness states and grouped safe next actions already exist | PMETH-03/04 refine five-method decisions, compatibility and proportionality |
| Runner/skills | routes.py builds methodology_packet; contracts/guards and lifecycle/requirements/test-eval skills exist | PMETH-05–17 connect decisions to artifacts/execution/evidence instead of recreating roles |
| CLI entrypoints | run_methodology_audit.py accepts workspace plus JSON/report; other entrypoints expose task intake | PMETH-01/02 select canonical adapters; an empty-intent default does not mean all engine paths lose intent |
| Infrastructure | Dry-run/stage/manifest/approval-aware merge and rollback exist | PMETH-12/16 reuse and verify that pipeline rather than another writer |
| Web/local service | Project Analysis already has a guarded HTTP route, Node service, Python bridge and project scan records. Current projection is project-level, and task-scoped advice is the gap | PMETH-19/20 extend the existing read-only path; PMETH-18/21 add persisted decisions and recovery where needed |
| Evidence | Python fixtures/evals, runner guards and Web checks exist | PMETH-22/23 verify end-to-end wiring; static/source evidence is not activation or model usefulness |

Main sources: `plugins/product-agent-os/scripts/product_agent_os/{discovery,methodology_audit,methodology_catalog,methodology_synthesis,task_routing,infrastructure,merge_infrastructure}.py`, `plugins/product-agent-os/scripts/codex_runtime_runner/{routes,contracts}.py` and canonical lifecycle/requirements/test-eval SKILL.md files. Use the [methodology intelligence guide](../product-agent-os/methodology-intelligence.en.md) alongside code; ambiguous mixed RU/EN wording is not independent evidence.

Methodology primary sources were checked in the preceding analysis on 2026-11-15 and are listed in [direction A](methodology-improvement-2026-11-15.en.md). This is a project-authored capability proposal, not a newly verified feature or a claim that Design-DD/ADD have one industry-standard definition.

## Intended user journey

| Step | User outcome | Verifiable result |
| --- | --- | --- |
| Context | Minimal project/task profile, constraints and missing context | Source-bound facts separate from assumptions |
| Selection | Applicable methods, reasons and depth | Reasons, applicability, owners, override/disposition and next action |
| Planning | One plan with requirements/design/boundaries/checks as needed | AC and dependency DAG without unnecessary ceremony |
| Preparation | Reviewable artifacts/proposals and exact diffs | Preserve authored files; no target change yet |
| Execution | One authorized slice, suitable skills/agents and checks | Authority, ownership, RED/GREEN where applicable and stop/recovery |
| Acceptance | Criterion evidence and honest gaps | Separate technical/model/human/release conclusions |

Method recommendations are not action permissions; selecting a profile does not start apply. Configuration/documents, detected structure, available capabilities, actual invocation and accepted outcomes require separate evidence.

## Product behavior for five methodologies

| Method | Proposed Product-Agent OS capability | Evidence of application |
| --- | --- | --- |
| Spec-DD | Concise/full requirements, AC/scenarios, canonical ownership, traceability and drift handling | Intent → criterion → scenario/check → receipt with revisions/owners |
| Design-DD | Journey/state matrices, design-system reuse, prototypes/accepted differences and visual/interaction plans | Changed journeys checked on current builds; mockups are not human acceptance |
| TDD | Risk/behavior-based strategy and observable RED → GREEN → REFACTOR | Intended failure before changed implementation; setup failures/test counts are not proof |
| ADD | Bounded context, ownership, skills/tools, budgets, stopping/handoff/recovery | Observed authorized execution and current receipts; evaluate model quality separately |
| FSD | Conditional suitability, source/import checks, ADR/public APIs and staged incremental migration | Verified boundaries/coverage and accepted checkpoints; folder names are insufficient |

## Different projects need different depth

| Scenario | Proportionate route | Do not impose |
| --- | --- | --- |
| Small backend bug | Concise scope/AC, reproduction/TDD, bounded ADD and regression | Full PRD, visual redesign or FSD |
| Greenfield frontend | First vertical slice, spec/journeys/states and minimal architecture choice | Empty layers, multi-team structure or scaffolding before decisions/authority |
| Coupled legacy frontend | Read-only map, characterization, architecture alternatives and one bridged pilot | Mass moves or overwriting existing rules |
| Already modular frontend | Verify existing boundaries and retain sufficient architecture | Folder renaming for an FSD label |
| Native/mobile | Platform/journey checks where applicable, specs/TDD/ADD | Frontend FSD based only on package.json |
| AI/RAG | Behavior specs and baseline evals; TDD for deterministic tools/logic | Unit passes as LLM-quality proof or hidden provider calls |
| Docs-only/read-only | Relevant reads, concise results and source/static checks for changes | Build gates, marker writes or unauthorized target control-plane setup |

## Stages and priorities

P1 is the required correctness/authority foundation before enabling the relevant route. P2 covers user integration, extended proposals, usefulness and delivery. Priority means neither a production incident nor automatic authority. A P2 dependency is mandatory for its dependent route.

### Delivery groups

Groups organize tasks by outcome. Each task can start when its own `depends_on` and applicable selection conditions are satisfied.

| Group | Tasks | Start and outcome |
| --- | --- | --- |
| **B1. Method selection and first CLI recommendation** | 01, 02, 22, 03, 04, 05, 07 | In the 01 → 02 → 22 → 03 → 04 → 05 → 07 sequence, record expected outcomes before changing the rules. In the same project, the CLI explains how to reproduce a backend bug and which test to run, and recommends a source check for a documentation edit. |
| **B2. Web recommendation, usefulness evaluation and rollout decision** | 19, 20, 26, 23, 24, 25 | After 07, tasks 19 → 20 → 26 present the recommendation in the existing task UI and document examples in Russian and English. Then 23 → 24 → 25 qualify the claimed profile, evaluate usefulness and decide the scope of rollout. Repeat 23 when expanding the profile. |
| **B3. Methods for UI design and frontend architecture** | 08, 09, 10, 11, 12 | After 05, the 08 → 09 branch specifies and verifies UI states. After 04, the 10 → 11 → 12 branch assesses FSD applicability, checks imports and prepares a migration proposal. Select the branches independently. Preparing the proposal requires only read access. |
| **B4. Execution, evidence and recovery** | 06, 13, 14, 15, 16, 17, 18, 21 | Task 06 tracks specification changes. Tasks 13–15 define ownership, skills and the execution plan. Task 16 covers preview and writes, 17 covers criterion-level evidence, 18 persists decisions, and 21 handles stopping and recovery. Each capability follows its own task dependencies. |

**B1 status.** Seven of seven tasks implemented and locally verified. The CLI returns a named test for the backend defect and a source check for the documentation task in the same disposable project. Next dependency is PMETH-19. [Local checks and handoff](../superpowers/specs/paos-pmeth-b1-evidence.en.md).

**B2 status.** Six of six tasks complete. The read-only CLI/Web profile is locally qualified, the four-run pilot returned insufficient evidence of benefit, and the owner approved a release `hold`. [Evidence and disposition](../superpowers/specs/paos-pmeth-b2-evidence.en.md).

**B3 status.** All five tasks complete. Design journeys and F14 findings were verified locally. A migration proposal requires complete relevant coverage. B4 entry points PAOS-PMETH-06 and PAOS-PMETH-13 meet their dependencies. [B3 evidence](../superpowers/specs/paos-pmeth-b3-evidence.en.md).

**B4 status.** All eight cards have local verification. The CLI explains drift and plans dependent work. Web/Desktop separates technical observations from owner dispositions and recovers through existing checkpoints. Write evidence comes from disposable targets. [B4 evidence](../superpowers/specs/paos-pmeth-b4-evidence.en.md).

**First accepted outcome: read-only CLI+Web.** Hard prerequisites: PMETH 01 → 02 → 22 → 03 → 04 → 05 → 07 → 19 → 20 → 26. In one disposable project, backend bug and docs-only give matching CLI/Web decisions with the same data and coverage, as well as reasons and the next verifiable step. PMETH-26 captures verified RU/EN examples. Acceptance requires observed CLI/HTTP/browser checks and negatives, plus a comprehension observation or explicit gap. PMETH-06, PMETH-08–18 and PMETH-21/23–25 are outside this milestone’s prerequisites.

**Extended route.** PMETH-15 connects selected slices. PMETH-16 adds apply, PMETH-17 adds technical evidence, and PMETH-18/21 add persisted decisions and recovery. PMETH-23 qualifies claimed profiles, PMETH-24 measures usefulness and PMETH-25 decides expansion. Design/FSD gates apply to their corresponding profiles. JSON has 31 active edges. `planning_revision` records the initial 54-edge graph and shifts of write, override and documentation responsibility. See the 2026-11-18 review in `research/methodology-plan-review-2026-11-18.md`.

## Conditional requirements before profile qualification

| Claimed route | Required task before profile-specific PMETH-23 |
| --- | --- |
| Base read-only bug/docs | PAOS-PMETH-26 |
| Design journey | PAOS-PMETH-09 |
| FSD migration | PAOS-PMETH-12 |
| Skill/tool routing | PAOS-PMETH-14 |
| Target writes | PAOS-PMETH-16 |
| Technical readiness by AC | PAOS-PMETH-17 |
| Durable override and recovery | PAOS-PMETH-21 |

Base PMETH-23 depends on PMETH-26. Before go on an additional claim, its listed task, hard prerequisites and profile-specific E2E evidence at the selected scope/revision are mandatory. Broad rollout qualifies every row. PMETH-25 reconciles task status and evidence against `profile_qualification`. Exclude unverified claims, and block an affected profile on a critical gap. Repeat PMETH-23 for the new scope and revision before expansion.

## Links to A and existing plans

- Retained METH-16 is reference-only; this B plan owns implementation. Legacy AC01 maps to PMETH-10/22, AC02 to PMETH-03/07/11, AC03 to PMETH-16/17/23/26. Retain old AC/IDs. Remove old METH-05/18 → METH-16 edges from the active DAG; they do not gate B.
- A owns METH-01–15/17/18; its scaling decision applies to internal METH-14/15. No cross-direction hard dependencies.
- Reuse FUNC-G01/F08 contract boundaries, discovery/renderer/merge and runner. F30's import-only PoC does not establish an installed complete graph engine; PMETH-11 uses confirmed adapters only.
- F02/F28/F25, F11/F12/F15/F16, F19/F21/F22/F23/F24 and UI-12 retain scope/status. B neither closes them automatically nor waits for every FUNC group. Recheck owners/regression/docs when changing shared contracts.
- Exclude new Files/Database/usages, M5 hosting/auth/team storage, telemetry billing, installation and commercial release without separate decisions.
- JSON external_refs are ownership/evidence references, not hard dependencies or another status authority. Recheck existing capability prerequisites on current source before a slice; if genuinely missing, refine dependencies with the canonical owner instead of assuming completion.

## Future slice verification

These are proposed acceptance profiles; TEST.md retains current verification routing and is unchanged.

| Profile | Minimum future checks |
| --- | --- |
| PV-PLAN / PV-DOCS | Source/semantic/link/parity checks and affected docs routing; task matrices/DAG; no runtime claims |
| PV-ENGINE | Focused methodology/catalog/synthesis/task-routing tests plus relevant PMETH-22 cases; baseline/candidate for behavior/prompt changes |
| PV-CONTRACT | Python/TS schema/adapter roundtrip, malformed/unknown/version/revision/project negatives and compatibility |
| PV-TDD | Intended RED, minimal GREEN and scoped refactor; preserve assertions/unique tests and explicit unavailable gaps |
| PV-DESIGN | Changed journey/state/visual/keyboard plan; current-build comparison when authorized; separate design/human acceptance |
| PV-FSD | Supported JS/TS/TSX imports/aliases/public APIs/cycles, partial coverage, no mutation and reviewable findings |
| PV-ADD | Ownership/context/tool/permission/timeout/partial/fallback negatives against baseline/candidate; separate prompt/model quality |
| PV-STAGE | Existing renderer/merge tests; dry-run → outside-target staging → reviewed fixture apply → rollback, drift/symlink/dirty-user preservation |
| PV-EVIDENCE | Criterion/receipt/readiness mapping, stale/forged/failure negatives and source/runtime provenance by claim |
| PV-STORAGE | Synthetic SQLite compatibility/migration/CAS/isolation/backup/restore; no real user DB |
| PV-BRIDGE | Actual adapters/API paths/selectors, negative old/fallback proof, session/origin/CSRF/project guards and qualification for affected runtime pins |
| PV-UI | Type-check/build and scoped current-build synthetic browser checks in both themes, RU/EN, keyboard/focus/errors; no providers/real credentials |
| PV-RECOVERY | Matching checkpoints, Stop/unknown/restart/no-replay, drift/concurrency/audit redaction and data preservation |
| PV-EVAL | Expected scenario outcomes before candidates, actual baseline/failure receipts and positive/edge/adversarial/regression scope without fictitious passes |
| PV-E2E | Disposable targets, actual chosen CLI/API/UI adapters, inside/outside authority, evidence and cleanup; separate models/humans |
| PV-ACTUAL | Comparable authorized actual-agent baseline/candidate, outcomes/effort/available costs and limits |
| PV-DECISION | Owner-reviewed supported scope, gap dispositions, rollback/disable and no external actions from decisions alone |

Take exact commands from TEST/current entrypoints; future commands are not checks executed today. Run full suites only for affected-contract/unknown-blast-radius/release triggers, not unchanged inputs. Unavailable model/host checks remain gaps; deterministic fixtures do not replace actual-agent quality.

## Authority, data, stopping and rollout

Default target access is read-only; existing user grants apply only inside their exact boundaries. Staging/proposals/profiles/graphs confer no approval. Target writes, installation, providers/cost, credentials, Git, deployment/publication, hooks/trust and external automation require applicable authority; later local synthetic acceptance does not authorize real projects/DBs.

Do not persist secrets, private raw chats, credentials, pairing/session material or unnecessary private project content. Prefer relative paths, revisions, selected facts and redacted receipts. Treat workspace/docs/MCP/tool content as untrusted data. Methodology selection cannot change instruction precedence or sandboxing.

Stop for unverified sources/authority, stale approvals, overlap, data loss/replay, permission violations, unknown parser coverage or unavailable material checks. Provide safe read-only/manual next actions without bypasses or silent fallbacks. Roll back only owned approved changes/managed sections/compatible state, preserving user files and avoiding destructive Git. Critical gaps block relevant acceptance rather than unrelated projects.

Critical criteria: zero unauthorized writes, lost user files, replayed unknown effects or false readiness from detection/missing/stale evidence. Define usefulness/latency/cost thresholds before actual candidate runs in PMETH-22/24; missing measurements are not zero or improvement. Permit bounded_go for supported CLI/profiles or hold/no-go; do not infer broad production usefulness/autonomous delivery from this plan.

## Historical verification of the 2026-11-15 revision

This verifies plan preparation, not A/B execution. Review mode: self_review; no independent/runtime/model/human acceptance is claimed.

- Four RU/EN A/B task matrices checked with `python -B plugins/product-agent-os/scripts/validate_task_matrix.py` and the corresponding plan: ok, errors=[].
- `python -B .docs-tools/reports/methodology-split-2026-11-15/verify_split.py verify` — ok: A17 + B26 executable tasks, one retained reference, 155 active AC plus three legacy AC; A25/B54 reciprocal edges, acyclic independent DAGs, RU/EN/JSON parity and baseline-before-policy.
- Preservation restored original A text by reversing only current planning hunks; retain all 18 prior IDs/titles/statuses and legacy AC. The two refined METH-05/18 criteria retain before-images in JSON history.
- Preserve existing shared documents outside owned METH sections; concurrent FUNC-G03 sections/source changes were not reverted. Source hashes are snapshots, not assertions of no changes in another workstream.
- `python -B tools/check_docs.py --paths` for 11 changed Markdown owners — OK; site/archive not checked. `git diff --check --` for the 13 owning plan/JSON/pointer paths — exit 0.
- Initial preflight stopped on a concurrent root change; source reads confirmed separate G03 scope and only exact METH hunks were applied. Large inline shell validation could not launch through the packaged shell; the local helper ran through system PowerShell without installation or policy changes.
- Control-plane sync: updated REQUIREMENTS/PLAN/RUNLOG METH sections, catalogs and registries; TEST/EVALS/prod_test no_change_needed. This task changed/executed no application code, active skills/workflows/hooks, targets, browser/native/provider/model/install/Git/publication. All implementation timestamps remain pending_execution_timestamp.

## Direction B task index

| ID | Priority | Group / methods | Task | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-PMETH-01 | P1 | B1; Spec-DD, ADD | Audit the existing methodology path and assign owners | — |
| PAOS-PMETH-02 | P1 | B1; Spec-DD, ADD | Normalize project profiles and user intent | PAOS-PMETH-01 |
| PAOS-PMETH-03 | P1 | B1; Spec-DD, Design-DD, TDD, ADD, FSD | Select proportionate methodologies and explain decisions | PAOS-PMETH-22 |
| PAOS-PMETH-04 | P1 | B1; Spec-DD, ADD | Define a versioned methodology contract | PAOS-PMETH-03 |
| PAOS-PMETH-05 | P1 | B1; Spec-DD | Integrate a Spec-Driven route from intent to verifiable specification | PAOS-PMETH-04 |
| PAOS-PMETH-06 | P1 | B4; Spec-DD, ADD | Track specification changes and stale context | PAOS-PMETH-05 |
| PAOS-PMETH-07 | P1 | B1; TDD, Spec-DD | Integrate TDD and bug reproduction into slice execution | PAOS-PMETH-05 |
| PAOS-PMETH-08 | P1 | B3; Design-DD, Spec-DD | Integrate Design-Driven journeys and state matrices | PAOS-PMETH-05 |
| PAOS-PMETH-09 | P1 | B3; Design-DD, TDD | Verify UI against the accepted design contract | PAOS-PMETH-08 |
| PAOS-PMETH-10 | P1 | B3; FSD, Spec-DD | Determine FSD applicability and propose architecture choices | PAOS-PMETH-04 |
| PAOS-PMETH-11 | P1 | B3; FSD, TDD | Verify frontend dependencies from source | PAOS-PMETH-10 |
| PAOS-PMETH-12 | P2 | B3; FSD, Spec-DD | Create incremental FSD migration proposals for user projects | PAOS-PMETH-11 |
| PAOS-PMETH-13 | P1 | B4; ADD, Spec-DD | Integrate ADD execution and ownership contracts | PAOS-PMETH-04 |
| PAOS-PMETH-14 | P2 | B4; ADD | Connect methodology decisions to available skills and tools | PAOS-PMETH-13 |
| PAOS-PMETH-15 | P1 | B4; Spec-DD, Design-DD, TDD, ADD, FSD | Compose methodologies into one proportionate delivery plan | PAOS-PMETH-07, PAOS-PMETH-13 |
| PAOS-PMETH-16 | P1 | B4; Spec-DD, ADD, FSD | Integrate safe staging, previews and authorized application | PAOS-PMETH-06, PAOS-PMETH-15 |
| PAOS-PMETH-17 | P1 | B4; Spec-DD, TDD, Design-DD, ADD, FSD | Collect evidence and compute criterion-based readiness | PAOS-PMETH-06, PAOS-PMETH-15 |
| PAOS-PMETH-18 | P2 | B4; Spec-DD, ADD | Define durable methodology state in Web/desktop | PAOS-PMETH-17, PAOS-PMETH-19 |
| PAOS-PMETH-19 | P2 | B2; ADD, Spec-DD | Connect the Python methodology engine to application API/runtime | PAOS-PMETH-07 |
| PAOS-PMETH-20 | P2 | B2; Design-DD, Spec-DD | Expose methodology choices, plans and evidence in the UI | PAOS-PMETH-19 |
| PAOS-PMETH-21 | P1 | B4; ADD, Spec-DD | Handle drift, stopping, resumption and audit | PAOS-PMETH-16, PAOS-PMETH-18, PAOS-PMETH-20 |
| PAOS-PMETH-22 | P1 | B1; Spec-DD, Design-DD, TDD, ADD, FSD | Prepare user-project baseline and acceptance eval matrices | PAOS-PMETH-02 |
| PAOS-PMETH-23 | P1 | B2; Spec-DD, Design-DD, TDD, ADD, FSD | Run end-to-end synthetic acceptance of the methodology path | PAOS-PMETH-26 |
| PAOS-PMETH-24 | P2 | B2; ADD, Spec-DD | Evaluate usefulness with comparable actual-agent pilots | PAOS-PMETH-23 |
| PAOS-PMETH-25 | P2 | B2; ADD, Spec-DD | Make a bounded delivery and rollout decision | PAOS-PMETH-24 |
| PAOS-PMETH-26 | P2 | B2; Spec-DD, Design-DD | Prepare user guidance and operator documentation | PAOS-PMETH-20 |

## Detailed direction B task cards

### Task `PAOS-PMETH-01`

- Task: PAOS-PMETH-01
- Task name: Audit the existing methodology path and assign owners
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: None.
- Blocks: PAOS-PMETH-02
- External references: PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Audit and extend existing components instead of building a parallel methodology engine.
- Technical value: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Product value: Avoid rebuilding working components.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `apps/local-service/src/project-analysis/bridge.py`, `apps/local-service/src/http/application.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-01-AC01**: Trace CLI intake through discovery/audit/synthesis/task routing, Project Analysis through its Python bridge to Sources/Teams & Tasks, and G9/F13 separately for writes. Identify the real entry point, owner and existing tests at each edge.
  - **PAOS-PMETH-01-AC02**: Record the two existing discovery/audit traversals, their filters and a coverage difference. Reuse existing inventories and distinguish detection, observed projection, proposals and execution.
  - **PAOS-PMETH-01-AC03**: Choose one owner and an existing entrypoint for every new contract; do not create a duplicate engine.
  - **PAOS-PMETH-01-AC04**: List baseline fixtures, commands, revision and compatibility consumers; the audit does not change active target assets.

- Verification gates: PV-PLAN; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + explorer; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Next step: Next dependency PAOS-PMETH-02.

#### Completion Report

- status: implemented
- what was done: Mapped CLI, audit, Project Analysis and the separate write boundary. Verified different inventory filters.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-02.

### Task `PAOS-PMETH-02`

- Task: PAOS-PMETH-02
- Task name: Normalize project profiles and user intent
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-01
- Blocks: PAOS-PMETH-22
- External references: PAOS-FUNC-28
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Provide minimal reliable context for choosing process depth.
- Technical value: Normalized profile/intent receipts with provenance and compatibility tests.
- Product value: Receive a process appropriate to the task and environment.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`, `plugins/product-agent-os/scripts/run_methodology_audit.py`, `apps/local-service/src/project-analysis/bridge.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Normalized profile/intent receipts with provenance and compatibility tests.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-02-AC01**: Distinguish greenfield/legacy, surface, scale/coupling, risk, change mode, available checks and environment limits; repository size is not risk.
  - **PAOS-PMETH-02-AC02**: Pass one normalized intent and applicable AC to audit and routing. Define precedence between task_context and intent_hint and reject conflicting, mixed or malformed input or expose an explicit gap. Verify desktop/Python adapter input and CLI intake with equivalent bug/docs tasks. PMETH-19 verifies parity on the real HTTP path and PMETH-16 verifies staging. Preserve repository-only audit.
  - **PAOS-PMETH-02-AC03**: Give facts provenance/revision and separate assumptions/missing context; a material blocking question does not replace available reads.
  - **PAOS-PMETH-02-AC04**: Docs-only, small bugfix and backend-only work do not receive full product ceremony or frontend gates.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Normalized profile/intent receipts with provenance and compatibility tests.
- Next step: Next dependency PAOS-PMETH-22.

#### Completion Report

- status: implemented
- what was done: Normalized intent, criteria and project profile. Checked CLI/Python parity, conflicting, incomplete and mixed input, and legacy audit.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-22.

### Task `PAOS-PMETH-03`

- Task: PAOS-PMETH-03
- Task name: Select proportionate methodologies and explain decisions
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-22
- Blocks: PAOS-PMETH-04
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Produce explainable proportionate decisions for all five methodologies.
- Technical value: Explainable decisions for five methodologies and baseline/candidate routing evidence.
- Product value: Understand method choices and avoid unnecessary process.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Explainable decisions for five methodologies and baseline/candidate routing evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-03-AC01**: For each methodology return applicability, reason, evidence refs, depth, owner and smallest next action; retain the existing 12 domains.
  - **PAOS-PMETH-03-AC02**: Use TDD for changed testable behavior and Design-DD for journeys/UI; condition FSD on frontend coupling and provide compact/full Spec-DD variants.
  - **PAOS-PMETH-03-AC03**: Missing evidence yields a question, gap or present_unverified. In the read-only path users refine input and recompute advice without a write. PMETH-18/21 own durable overrides with rationale and scope and preserve mandatory checks.
  - **PAOS-PMETH-03-AC04**: PMETH-22 baseline/candidate cases show no blanket FSD/DDD/TDD mandate, hidden new gates or false readiness.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Explainable decisions for five methodologies and baseline/candidate routing evidence.
- Next step: Next dependency PAOS-PMETH-04.

#### Completion Report

- status: implemented
- what was done: Each of five methods reports applicability, depth, ownership and next action. Backend/docs were checked without frontend gates.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-04.

### Task `PAOS-PMETH-04`

- Task: PAOS-PMETH-04
- Task name: Define a versioned methodology contract
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-03
- Blocks: PAOS-PMETH-05, PAOS-PMETH-10, PAOS-PMETH-13
- External references: PAOS-FUNC-08
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Maintain one compatible contract across engine, runner and UI.
- Technical value: Canonical versioned contracts, adapters and compatibility tests.
- Product value: Keep CLI/runner/Web decisions consistent.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `packages/contracts/`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `packages/contracts/project-analysis.ts`, `packages/contracts/issues/task-profile.ts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Canonical versioned contracts, adapters and compatibility tests.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-04-AC01**: Choose a single schema owner and minimal Python/TypeScript adapters over existing contracts. Distinguish project-only facts from task-scoped advice and validate project/task identity, source/task revisions and evidence references at the boundary.
  - **PAOS-PMETH-04-AC02**: Provide explicit compatibility mappings for current readiness states, packets and legacy consumers; unknown/newer versions do not default to success.
  - **PAOS-PMETH-04-AC03**: Separate decisions, plans, execution receipts and acceptance verdicts; store no private raw chat/secrets or authority inferred from recommendations.
  - **PAOS-PMETH-04-AC04**: Contract tests cover roundtrip, malformed input, wrong project/task/revision and adapter parity; schema presence is not activation.

- Verification gates: PV-CONTRACT; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Canonical versioned contracts, adapters and compatibility tests.
- Next step: Next dependency PAOS-PMETH-05.

#### Completion Report

- status: implemented
- what was done: Python and TypeScript consume contract v1. Checked round-trip, unknown version, mismatched scope and faulty source links.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-05.

### Task `PAOS-PMETH-05`

- Task: PAOS-PMETH-05
- Task name: Integrate a Spec-Driven route from intent to verifiable specification
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-06, PAOS-PMETH-07, PAOS-PMETH-08
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Turn user intent into a verifiable contract for the selected slice.
- Technical value: Concise/full requirements proposals with AC traceability and assigned ownership.
- Product value: Accept outcomes against clear criteria.
- Scope: `plugins/product-agent-os/skills/requirements-author/SKILL.md`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py`, `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Concise/full requirements proposals with AC traceability and assigned ownership.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-05-AC01**: Give a small task concise scope/AC in the existing task or read-only projection without generating files. Route complex requirements, non-goals, invariants and scenarios to the existing owner.
  - **PAOS-PMETH-05-AC02**: Link every AC to an observable scenario/check/evidence owner or explicit gap; expose ambiguity/assumptions before build.
  - **PAOS-PMETH-05-AC03**: Preserve user-authored requirements and their owner. The read-only path shows the next step as text or a link. PMETH-16 owns staged proposals, diffs and application.
  - **PAOS-PMETH-05-AC04**: Do not scaffold greenfield work before selecting the first vertical slice and obtaining applicable authority; specification changes are not working-code proof.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + product-manager; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Concise/full requirements proposals with AC traceability and assigned ownership.
- Next step: Next dependency PAOS-PMETH-07.

#### Completion Report

- status: implemented
- what was done: Compact or full requirements link each criterion to a scenario, check or gap, and owner. Verified greenfield without creating files.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-07.

### Task `PAOS-PMETH-06`

- Task: PAOS-PMETH-06
- Task name: Track specification changes and stale context
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-16, PAOS-PMETH-17
- External references: PAOS-FUNC-02, PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Prevent stale-plan execution and retain requirement/evidence consistency.
- Technical value: Revision/impact/disposition records and stale-context regression evidence.
- Product value: Preserve decisions and avoid stale instructions.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py`; `plugins/product-agent-os/scripts/product_agent_os/documentation_sync.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Revision/impact/disposition records and stale-context regression evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-06-AC01**: Map AC/API/schema/source changes to affected slices/checks/owners; textual diffs are not complete semantic-impact proof.
  - **PAOS-PMETH-06-AC02**: Stale plans/proposals/receipts cannot promote readiness; resume requires current context/authority and preserves history.
  - **PAOS-PMETH-06-AC03**: Reassessment of unchanged inputs performs no repeated writes; conflicting edits require review/handoff rather than overwrite.
  - **PAOS-PMETH-06-AC04**: Synthetic concurrent edits, renamed artifacts, missing owners and changed acceptance have explicit outcomes and preservation checks.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Revision/impact/disposition records and stale-context regression evidence.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: The CLI compares task, criterion and source revisions and identifies the owners who need to review them.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-07`

- Task: PAOS-PMETH-07
- Task name: Integrate TDD and bug reproduction into slice execution
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-15, PAOS-PMETH-19
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Apply test-first where it validates behavior and explain exceptions honestly.
- Technical value: Test/eval routes, RED/GREEN receipts and justified exceptions.
- Product value: Receive reproducible fixes and regression protection.
- Scope: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/assets/templates/workflows/`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`, `tests/product_agent_os/test_codex_runtime_runner_cli.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Test/eval routes, RED/GREEN receipts and justified exceptions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-07-AC01**: Show the next test for a backend bug and a source check for docs-only in the read-only path. Substantiate one regression check on a synthetic fixture with intended observable RED, minimal GREEN and scoped refactor disposition. Capture command, revision and expected/actual in existing evidence without writing to the target.
  - **PAOS-PMETH-07-AC02**: Setup/import/tool-missing failures are not RED; retain the original reproducible failure after success.
  - **PAOS-PMETH-07-AC03**: Use characterization/regression for preserving refactors and appropriate static checks/evals for docs/config/subjective LLM outputs without artificial RED.
  - **PAOS-PMETH-07-AC04**: Unavailable checks remain explicit gaps; do not rewrite/delete assertions for green or use test counts as correctness proof.

- Verification gates: PV-TDD; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Test/eval routes, RED/GREEN receipts and justified exceptions.
- Next step: Next dependency PAOS-PMETH-19.

#### Completion Report

- status: implemented
- what was done: The CLI provides the backend test and docs source. Actual RED, minimal GREEN and the import-failure control have separate receipts.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-19.

### Task `PAOS-PMETH-08`

- Task: PAOS-PMETH-08
- Task name: Integrate Design-Driven journeys and state matrices
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-09
- External references: UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Design journeys and states before implementing changed user interactions.
- Technical value: Journey/state matrices, design references and acceptance boundaries.
- Product value: Check usability before expensive implementation.
- Scope: `tools/project-methodology.mts`; `tools/project-methodology/design.mts`; `tests/fixtures/product_agent_os/pmeth-b3-design.json`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Journey/state matrices, design references and acceptance boundaries.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-08-AC01**: Define the goal, steps, data, interaction/error/empty/loading/dirty states and accessibility for changed journeys. Record a problem hypothesis and representative user observation or evidence gap for substantial or uncertain journeys. Backend-only is not_applicable.
  - **PAOS-PMETH-08-AC02**: Reuse existing design/system and propose missing states separately; a new mockup is not user-approved by default.
  - **PAOS-PMETH-08-AC03**: Distinguish synthetic/current/unavailable data and real API constraints; do not promise unsupported states as available functions.
  - **PAOS-PMETH-08-AC04**: Separate design, implementation and human-acceptance ownership/evidence; small UI changes do not require full-project redesign.

- Verification gates: PV-ENGINE. [Executed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Journey/state matrices, design references and acceptance boundaries.
- Next step: 09 verifies the associated UI journey.

#### Completion Report

- status: implemented
- what was done: Goal, steps, data, state matrix and accessibility are bound to a revision.
- files touched / work locations: [Implementation paths and fixtures](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- technical value delivered: Revision-bound output with explicit evidence.
- product value delivered: Existing assets, proposed states and gaps remain visible.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Observed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- residual risks: Representative user observation is needed for a selected real journey.
- follow-up: 09 verifies the associated UI journey.

### Task `PAOS-PMETH-09`

- Task: PAOS-PMETH-09
- Task name: Verify UI against the accepted design contract
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-08
- Blocks: None.
- External references: PAOS-FUNC-19, UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Compare the running interface against accepted design contracts.
- Technical value: Current-build visual/interaction evidence or explicit unavailable gaps.
- Product value: See design-versus-runtime differences.
- Scope: `tools/project-methodology/design.mts`; `apps/web/src/design/parity.css`; `tests/web/single-window/methodology-advice-browser-acceptance.mts`; `tests/fixtures/product_agent_os/pmeth-b3-composition.json`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Current-build visual/interaction evidence or explicit unavailable gaps.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-09-AC01**: Select available component/browser/visual/keyboard checks for the changed journey, viewport/theme/long-content states and source/build/harness provenance.
  - **PAOS-PMETH-09-AC02**: Check composition/actions beyond overflow/contrast; detect intentional fixture mismatch and make baseline updates reviewable.
  - **PAOS-PMETH-09-AC03**: Screenshot/prototype passes are not human-usability acceptance, WCAG certification or API-side-effect proof.
  - **PAOS-PMETH-09-AC04**: If runtime/browser is unavailable or unauthorized, return a gap and safe next action without bypassing limits or substituting old screenshots.

- Verification gates: PV-DESIGN. [Executed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Current-build visual/interaction evidence or explicit unavailable gaps.
- Next step: Repeat PMETH-23 when expanding the profile.

#### Completion Report

- status: implemented
- what was done: States, accessibility and composition were compared with the versioned design contract.
- files touched / work locations: [Implementation paths and fixtures](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- technical value delivered: Revision-bound output with explicit evidence.
- product value delivered: The browser exercised both locales. Unavailable browser evidence leaves a gap.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Observed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#design-verification).
- residual risks: Technical checks cover the synthetic journey.
- follow-up: Repeat PMETH-23 when expanding the profile.

### Task `PAOS-PMETH-10`

- Task: PAOS-PMETH-10
- Task name: Determine FSD applicability and propose architecture choices
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-11
- External references: PAOS-FUNC-30
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Recommend FSD only with evidence of usefulness for the user frontend.
- Technical value: FSD applicability decisions and architecture proposals with alternatives.
- Product value: Choose architecture based on usefulness rather than fashion.
- Scope: `tools/project-methodology.mts`; `tools/project-methodology/architecture.mts`; `tests/web/project-methodology-b3.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: FSD applicability decisions and architecture proposals with alternatives.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-10-AC01**: Produce evidence-based distinct recommendations for small/static frontends, backend/native-only work, growing frontends and already-modular legacy.
  - **PAOS-PMETH-10-AC02**: Compare preserving architecture, strengthening boundaries and gradual FSD using coupling, change frequency, ownership and migration cost.
  - **PAOS-PMETH-10-AC03**: Start with pages and demonstrated coupling. Introduce public APIs and lower layers/slices where a need is demonstrated. Apply the relevant architecture policy to backend, Python and native targets.
  - **PAOS-PMETH-10-AC04**: An architecture proposal requires an applicable owner decision before migration; absence of FSD is not itself a defect.

- Verification gates: PV-ENGINE. [Executed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: FSD applicability decisions and architecture proposals with alternatives.
- Next step: 11 verifies public boundaries and owners.

#### Completion Report

- status: implemented
- what was done: Applicability uses observed imports and the current stack.
- files touched / work locations: [Implementation paths and fixtures](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- technical value delivered: Revision-bound output with explicit evidence.
- product value delivered: Recommendations distinguish static, modular and coupled frontends and other stacks.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Observed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- residual risks: Incomplete coverage yields partial with the reason.
- follow-up: 11 verifies public boundaries and owners.

### Task `PAOS-PMETH-11`

- Task: PAOS-PMETH-11
- Task name: Verify frontend dependencies from source
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-10
- Blocks: PAOS-PMETH-12
- External references: PAOS-FUNC-14, PAOS-FUNC-30
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Separate folder signals from verified code boundaries for supported languages.
- Technical value: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Product value: Receive verifiable architecture findings.
- Scope: `apps/local-service/src/code-index/lexical.mts`; `apps/local-service/src/code-index/resolver-config.mts`; `apps/local-service/src/code-index/service.mts`; `tools/project-methodology/architecture.mts`; `tests/web/graph-imports.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-11-AC01**: Evaluate FSD rules over observed F14 edges for JS/TS/TSX and bind results to the source revision. Explicitly check coverage of TSImportType, re-exports, tsconfig aliases/extends and literal dynamic imports.
  - **PAOS-PMETH-11-AC02**: Unsupported syntax, aliases, symlinks, out-of-scope source and CLI without an available adapter yield partial/unknown with coverage and an explanation. Partial graphs and folder signals cannot yield present_verified.
  - **PAOS-PMETH-11-AC03**: Report path/line/rule/owner for violations and distinguish valid entity public APIs and legacy exceptions.
  - **PAOS-PMETH-11-AC04**: Reuse F14 code-index, its parser/resolver and fixtures. Keep F30 as an import-only reference. Verify meaningful parser cases, cycles and no-source-mutation hashes without requiring installation.

- Verification gates: PV-FSD. [Executed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Next step: 12 consumes observations in its proposal.

#### Completion Report

- status: implemented
- what was done: Verified layers, public APIs, cycles, @x and narrow legacy exceptions.
- files touched / work locations: [Implementation paths and fixtures](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- technical value delivered: Revision-bound output with explicit evidence.
- product value delivered: The report gives the import, anchor, rule and owner.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Observed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#architecture-evidence).
- residual risks: Unsupported import forms explicitly limit coverage.
- follow-up: 12 consumes observations in its proposal.

### Task `PAOS-PMETH-12`

- Task: PAOS-PMETH-12
- Task name: Create incremental FSD migration proposals for user projects
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B3
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B3 local read-only implementation and synthetic verification.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:37
- Depends on: PAOS-PMETH-11
- Blocks: None.
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Plan minimal reversible migration under accepted boundaries.
- Technical value: Incremental migration plans with pilots/public APIs/rollback and staged diffs.
- Product value: Improve frontend structure incrementally without behavior loss.
- Scope: `tools/project-methodology/architecture.mts`; `tests/web/project-methodology-b3.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Read-only migration proposal with a reversible page pilot, public APIs, import ratchet and criteria for the next checkpoint.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-12-AC01**: Include baseline imports, a minimal pilot, AC, owners, dependencies, compatibility bridges and rollback; no mandatory full rewrite.
  - **PAOS-PMETH-12-AC02**: Start with a boundary and one page pilot with a public API/import ratchet. Extract to shared/entities where reuse is demonstrated. Later checkpoints require adoption of the previous one, and the pilot may be the stopping point.
  - **PAOS-PMETH-12-AC03**: Describe how the proposal preserves user files, dirty changes and business/API semantics, and how to check legacy import boundaries. Preserve target files in this task. PMETH-23 verifies actual code moves when included in the pilot scope.
  - **PAOS-PMETH-12-AC04**: Deliver the read-only proposal in memory. The separately selected FSD path uses the PMETH-16 writer for staged diff and apply, verified in PMETH-23. Target writes and hook activation require separate authority.

- Verification gates: PV-STAGE. [Executed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#migration-proposal).
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Read-only migration proposal with a reversible page pilot, public APIs, import ratchet and criteria for the next checkpoint.
- Next step: Target writes require separately authorized scope.

#### Completion Report

- status: implemented
- what was done: Produced a one-page proposal with baseline, re-export, import ratchet and rollback.
- files touched / work locations: [Implementation paths and fixtures](../superpowers/specs/paos-pmeth-b3-evidence.en.md#migration-proposal).
- technical value delivered: Revision-bound output with explicit evidence.
- product value delivered: The owner can stop after the first page and verify observed imports.
- actual implementation date and time: 19-11-2026 11:37
- verification evidence: [Observed checks](../superpowers/specs/paos-pmeth-b3-evidence.en.md#migration-proposal).
- residual risks: Execution depends on PMETH-16 and profile-specific PMETH-23.
- follow-up: Target writes require separately authorized scope.

### Task `PAOS-PMETH-13`

- Task: PAOS-PMETH-13
- Task name: Integrate ADD execution and ownership contracts
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-04
- Blocks: PAOS-PMETH-14, PAOS-PMETH-15
- External references: PAOS-FUNC-15, PAOS-FUNC-16
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Give agents bounded verifiable work without expanding authority.
- Technical value: Bounded agent contexts, ownership/budget/stop records and guard tests.
- Product value: Delegate bounded work with clear stopping.
- Scope: `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`; `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/guards.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Bounded agent contexts, ownership/budget/stop records and guard tests.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-13-AC01**: Pass goal/AC/source revision, allowed/forbidden paths, checks and stop/handoff; use concise routing for ordinary work.
  - **PAOS-PMETH-13-AC02**: Default to one agent; parallelize only independent ownership with permitted host capabilities and serialize overlapping files.
  - **PAOS-PMETH-13-AC03**: Follow current configured model/reasoning/tool budgets; a role does not create a sandbox or imply escalation/provider selection.
  - **PAOS-PMETH-13-AC04**: Unknown capabilities, timeouts, partial children and stale handoffs are not success; record no-silent-fallback decisions and bounded retries.

- Verification gates: PV-ADD; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: lifecycle-orchestrator + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Bounded agent contexts, ownership/budget/stop records and guard tests.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: Assignments bind scope, checks and stop conditions to the current context.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-14`

- Task: PAOS-PMETH-14
- Task name: Connect methodology decisions to available skills and tools
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-13
- Blocks: None.
- External references: PAOS-FUNC-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Connect decisions to available executors without hidden installation.
- Technical value: Skill/tool routes with provenance, capabilities and safe fallback dispositions.
- Product value: Use available capabilities without hidden environment changes.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/skills/references/`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Skill/tool routes with provenance, capabilities and safe fallback dispositions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-14-AC01**: Map each method to existing canonical skills/workflows and relevant inputs; do not load all skills or invent tool availability.
  - **PAOS-PMETH-14-AC02**: Distinguish installed/staged/exposed/invoked states; missing skills/tools produce safe manual/staged next actions and gaps.
  - **PAOS-PMETH-14-AC03**: Skill/MCP/doc content cannot increase authority; do not execute embedded instructions, malicious commands or external writes as recommendations.
  - **PAOS-PMETH-14-AC04**: Keep install/connect/activation separately authorized; model prompts contain no secrets or raw private chats.

- Verification gates: PV-ADD; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Skill/tool routes with provenance, capabilities and safe fallback dispositions.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: Applicable methods select canonical skills and workflows with explicit availability evidence.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-15`

- Task: PAOS-PMETH-15
- Task name: Compose methodologies into one proportionate delivery plan
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-07, PAOS-PMETH-13
- Blocks: PAOS-PMETH-16, PAOS-PMETH-17
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Produce one delivery DAG with the minimum necessary gates.
- Technical value: A single delivery DAG linking methods to each slice.
- Product value: Use one consistent plan rather than competing queues.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: A single delivery DAG linking methods to each slice.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-15-AC01**: Build one DAG over methodology_synthesis and formation_plan. The canonical name and alias of one existing file produce one artifact and one owner with both reasons.
  - **PAOS-PMETH-15-AC02**: Record actual prerequisites. PMETH-08/09 and PMETH-10–12 apply only to Design/FSD branches and PMETH-14 adds skills as needed. Compact bug/docs advice is available through PMETH-19/20 without the delivery DAG.
  - **PAOS-PMETH-15-AC03**: Each slice has input/output/owner/AC/checks/stop; apply relevant gates to backend/API/AI paths and evals to subjective AI quality.
  - **PAOS-PMETH-15-AC04**: Cycles/conflicts/accepted gaps produce explainable next actions; methodology advice neither expands authority nor starts execution automatically.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: A single delivery DAG linking methods to each slice.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: An explicit mode composes methods and artifact owners into one dependency graph.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-16`

- Task: PAOS-PMETH-16
- Task name: Integrate safe staging, previews and authorized application
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-06, PAOS-PMETH-15
- Blocks: PAOS-PMETH-21
- External references: PAOS-FUNC-13
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Use the existing approval-aware pipeline without losing user-authored files.
- Technical value: Stage/preview/approval/apply/rollback receipts for fixture targets.
- Product value: Preserve authored files and control proposal application.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/merge_infrastructure.py`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/project_formation.py`, `packages/contracts/artifacts/document-apply.ts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Stage/preview/approval/apply/rollback receipts for fixture targets.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-16-AC01**: Use G9 formation/dry-run/stage/manifest/merge for infrastructure bundles and F13 document apply for eligible single-document proposals. Each operation kind selects one writer, the stage stays outside the target and writes require exact authority.
  - **PAOS-PMETH-16-AC02**: Use the existing preview to show owned paths, user-file handling, method/AC links, side effects and writer. Preserve unmarked AGENTS/config/hooks and expose apply only through its own route.
  - **PAOS-PMETH-16-AC03**: Bind preview/apply to an exact digest, project/task, revision and operation ID. Reject drift, wrong root/project, traversal/symlinks and stale approvals. Preserve edits in recovery and prevent replay of effects with unknown outcomes.
  - **PAOS-PMETH-16-AC04**: Synthetic apply/rollback uses fixture targets and verifies byte preservation; proposals do not activate hooks/automation/install/providers.

- Verification gates: PV-STAGE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Stage/preview/approval/apply/rollback receipts for fixture targets.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: G9 and F13 bind approval to reviewed revisions and preserve independent edits and recovery history.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-17`

- Task: PAOS-PMETH-17
- Task name: Collect evidence and compute criterion-based readiness
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, TDD, Design-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-06, PAOS-PMETH-15
- Blocks: PAOS-PMETH-18
- External references: PAOS-FUNC-02
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Support readiness for every applicable check with current evidence.
- Technical value: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Product value: Distinguish evidence-backed outcomes from plans and assumptions.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`, `apps/local-service/src/tasks/user-commands.mts`, `apps/local-service/src/workflows/guards.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-17-AC01**: Trace requirement through stable AC ID, scenario/check and receipt to a verdict with owner, revision/environment and applicability. Preserve manual acceptance for two ACs in a synthetic task. Technical evidence counts only for the AC with a bound receipt at the correct revision. Keep accepted gaps distinct.
  - **PAOS-PMETH-17-AC02**: Reuse task_routing input_digest/check_observations and existing receipts/acceptTask. Caller-reported results, detection, generated files and test counts cannot produce technical passed. Keep missing/stale/failed/partial visible.
  - **PAOS-PMETH-17-AC03**: Use runtime evidence for implementation/provider-path claims when required and authorized; unit smoke is not activation.
  - **PAOS-PMETH-17-AC04**: The CLI pilot links applicable methods to checks on one fixture revision, separating technical, manual/human and release acceptance. Visual, FSD and target-apply evidence supports corresponding PMETH-23 claims.

- Verification gates: PV-EVIDENCE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: Technical observations bind one criterion to a current revision independently of owner acceptance.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-18`

- Task: PAOS-PMETH-18
- Task name: Define durable methodology state in Web/desktop
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-17, PAOS-PMETH-19
- Blocks: PAOS-PMETH-21
- External references: PAOS-FUNC-02, PAOS-FUNC-08, PAOS-FUNC-22, PAOS-FUNC-28, PAOS-FUNC-29
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Persist consistent project/task state without a second status authority.
- Technical value: Durable profile/decision/evidence models and synthetic migration/recovery checks.
- Product value: Resume with consistent project/task state.
- Scope: `packages/contracts/`; `apps/local-service/src/storage/`; `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/artifacts/service.mts`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `apps/local-service/src/project-scans/service.mts`, `packages/contracts/issues/task-profile.ts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Durable profile/decision/evidence models and synthetic migration/recovery checks.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-18-AC01**: Use scans, tasks/links and evidence as canonical owners for project facts, task advice, persisted decisions and criterion evidence. Add durable records only for proven gaps. PMETH-19 reads require no migration.
  - **PAOS-PMETH-18-AC02**: Support version/revision/CAS, history, project isolation and explicit unknown. Store override reason, scope, actor and revisions while retaining mandatory checks. Preserve data across older clients and newer schemas.
  - **PAOS-PMETH-18-AC03**: If needed, validate additive/recoverable migrations with synthetic backup/restore and compatibility checks; do not access/migrate real user DBs in this slice.
  - **PAOS-PMETH-18-AC04**: Store no secrets/private raw chat; missing token/cost telemetry remains null/unavailable without expanding into F11.

- Verification gates: PV-STORAGE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + builder — storage/contracts; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Durable profile/decision/evidence models and synthetic migration/recovery checks.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: Web/Desktop persists the disposition, scope, actor and history with revision checks.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-19`

- Task: PAOS-PMETH-19
- Task name: Connect the Python methodology engine to application API/runtime
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-07
- Blocks: PAOS-PMETH-18, PAOS-PMETH-20
- External references: PAOS-FUNC-01, PAOS-FUNC-08, PAOS-FUNC-27
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Connect the existing methodology engine to an observable application path.
- Technical value: Versioned bridge/API and current-path activation/negative receipts.
- Product value: Use an observable methodology path in the application.
- Scope: `apps/local-service/src/http/application.mts`; `apps/local-service/src/runtime/`; `packages/contracts/`; `plugins/product-agent-os/scripts/product_agent_os/`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `apps/local-service/src/project-analysis/bridge.py`, `apps/local-service/src/project-analysis/service.mts`, `apps/local-service/src/project-scans/service.mts`, `packages/contracts/project-analysis.ts`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Read-only task advice through the existing Project Analysis API, CLI parity, partial/last relevant stage and negative receipts.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-19-AC01**: The guarded Project Analysis HTTP path through its Python bridge returns task-scoped advice separately from project facts. Equivalent bug/docs requests with the same data and coverage yield the same decisions and reasons in CLI. When Web sees only metadata and CLI reads source, explain the difference through coverage and partial/unknown. Reject wrong project/task/revision and unsupported schema responses.
  - **PAOS-PMETH-19-AC02**: Check session/origin/project scope, input bounds and cancellation for read-only requests. Apply CSRF according to HTTP method and the existing contract. Reads require no target write or new durable store. PMETH-16/21 own the mutating route and its authority checks.
  - **PAOS-PMETH-19-AC03**: Expose intended path/selector, partial/ready/warnings and the reason. After analysis then schema/code_database, opening advice retains the last relevant analysis stage for the required revision or explains the next step. Surface bridge failures without masking fallbacks.
  - **PAOS-PMETH-19-AC04**: The bridge calls no model/provider, runs no arbitrary repo command and uses no real credentials; pinned-source changes follow TEST qualification.

- Verification gates: PV-BRIDGE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: builder — local-service + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Read-only task advice through the existing Project Analysis API, CLI parity, partial/last relevant stage and negative receipts.
- Next step: PAOS-PMETH-20

#### Completion Report

- status: implemented
- what was done: Connected guarded HTTP to the isolated Python bridge. Verified CLI/Web parity, scope, failures and cancellation.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- technical value delivered: Verified in the approved B2 scope.
- product value delivered: An observable recommendation for a saved task.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- expanded qualification: [PMETH-23, B3/B4 profiles](../superpowers/specs/paos-pmeth-23-expanded-evidence.en.md#create-recovery-closure). Result `implemented_locally_verified`. Recovery passed for `create` and `modify` with adapter revision `05fbd1d086c8411c1ad689bbdf02671e17db3da706a5691c467f30080846d5a9`.
- residual risks: The release remains on hold. Live-session skill invocation, usefulness, and human acceptance require separate evidence.
- follow-up: PAOS-PMETH-20.

### Task `PAOS-PMETH-20`

- Task: PAOS-PMETH-20
- Task name: Expose methodology choices, plans and evidence in the UI
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-19
- Blocks: PAOS-PMETH-21, PAOS-PMETH-26
- External references: PAOS-FUNC-23, PAOS-FUNC-24, PAOS-FUNC-27, UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Help users understand choices, limitations and next actions.
- Technical value: Approved UI flows, selected-scope implementation and browser evidence.
- Product value: Understand next actions, limits and stopping reasons.
- Scope: `apps/web/src/ui/App.tsx`; `apps/web/src/features/tasks/`; `apps/web/src/features/projects/`; `apps/web/src/locales/`; `docs/frontend/`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `apps/web/src/features/projects/project-analysis.css`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Read-only bug/docs flow in Sources and Teams & Tasks, synthetic browser evidence and a comprehension observation or explicit gap.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-20-AC01**: Show project facts in Sources and task advice and the next verifiable step in the existing Teams & Tasks flow. Agree on minimal placement and states, and show rationale, depth and required/optional/not_applicable.
  - **PAOS-PMETH-20-AC02**: Show source/coverage/unknown, scope, permissions and stop reasons. Check whether a person can explain the advice, identify the next step and distinguish viewing from applying without prompting. Record the observation or evidence gap under PMETH-22.
  - **PAOS-PMETH-20-AC03**: Verify loading/empty/error/stale/partial and applicable permission-required, RU/EN, themes and keyboard/focus. Partial shows available facts and warnings, and backend unavailability is never replaced by fixture success. PMETH-21/23 verify conflict and apply for writes.
  - **PAOS-PMETH-20-AC04**: Exercise the PMETH-19 API from a synthetic browser for backend bug and docs-only, including wrong project/task, partial output and latest scan stage changes. Preserve the target and durable methodology state. PMETH-18/21 own persisted override and audit.

- Verification gates: PV-UI; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + builder — web; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Read-only bug/docs flow in Sources and Teams & Tasks, synthetic browser evidence and a comprehension observation or explicit gap.
- Next step: PAOS-PMETH-26

#### Completion Report

- status: implemented
- what was done: The existing task summary shows advice. Verified both locales and themes, keyboard and result states. Human comprehension remains an evidence gap.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- technical value delivered: Verified in the approved B2 scope.
- product value delivered: An observable recommendation for a saved task.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- residual risks: The release remains on hold. Expanded profile and human comprehension need separate evidence.
- follow-up: PAOS-PMETH-26.

### Task `PAOS-PMETH-21`

- Task: PAOS-PMETH-21
- Task name: Handle drift, stopping, resumption and audit
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 13:14
- Depends on: PAOS-PMETH-16, PAOS-PMETH-18, PAOS-PMETH-20
- Blocks: None.
- External references: PAOS-FUNC-21
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Resume safely after context changes or stopping.
- Technical value: Drift/stop/resume/audit records and replay/data-preservation checks.
- Product value: Recover without replaying side effects.
- Scope: `apps/local-service/src/runtime/`; `apps/local-service/src/sessions/`; `apps/local-service/src/storage/`; `plugins/product-agent-os/scripts/codex_runtime_runner/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Drift/stop/resume/audit records and replay/data-preservation checks.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-21-AC01**: Task/source/profile/permission revision changes invalidate dependent authority/readiness; replans explain affected scope without automatic target writes.
  - **PAOS-PMETH-21-AC02**: Stop/cancel and unknown outcomes do not replay effects; resume requires matching project/task/checkpoint and current permissions.
  - **PAOS-PMETH-21-AC03**: Preserve minimal audit records with redaction, owner and time. Show manual overrides/dispositions in the existing task and preserve partial/failed attempts. Preview/apply shows digest/revision, diff, conflict and authority state.
  - **PAOS-PMETH-21-AC04**: Synthetic-test restart/bridge failure/concurrent edits/budget exhaustion with visible next actions; claim no unattended automation or closed-App operation.

- Verification gates: PV-RECOVERY; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: builder — runtime + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Drift/stop/resume/audit records and replay/data-preservation checks.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: implemented
- what was done: The task shows an unknown outcome and directs recovery to the existing checkpoint.
- files touched / work locations: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- technical value delivered: Verified the local execution contract and its negative cases.
- product value delivered: The task has a reviewable next action and evidence tied to its scope.
- actual implementation date and time: 19-11-2026 13:14
- verification evidence: [B4](../superpowers/specs/paos-pmeth-b4-evidence.en.md)
- residual risks: Extended PMETH-23 profile qualification and owner release approval remain separate.
- follow-up: Keep the approved release hold.

### Task `PAOS-PMETH-22`

- Task: PAOS-PMETH-22
- Task name: Prepare user-project baseline and acceptance eval matrices
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized bounded B1 implementation following the plan review.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 20:43
- Depends on: PAOS-PMETH-02
- Blocks: PAOS-PMETH-03
- External references: PAOS-FUNC-23
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Define expected behavior and baselines before changing routing.
- Technical value: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Product value: Receive routing checked on ordinary and negative cases.
- Scope: `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_methodology_synthesis.py`; `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`; `plugins/product-agent-os/assets/fixtures/`. Future work locations; PMETH-01 refines exact owned files before execution. Modules and checks to reuse: `tests/product_agent_os/test_codex_runtime_runner_cli.py`, `tests/web/project-analysis-api.test.mts`.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-22-AC01**: PMETH-22 completes its baseline before policy changes on two tasks in one project, backend bug and docs-only. Set AC, next test or source link, reasons and gaps in advance. Retain native, AI/RAG and three frontend profiles in the scenario matrix. Branch owners capture their baseline before candidate checks and enabling each profile.
  - **PAOS-PMETH-22-AC02**: Early negatives cover conflicting/incomplete intent, missing tests, stale/partial output, wrong project/task/revision and absence of target writes. Keep misleading folders, unknown aliases, stale specs, forged success, prompt injection, dirty files, denied writes and unavailable tools in the shared matrix. The owning branch checks them before enabling.
  - **PAOS-PMETH-22-AC03**: Preserve baseline results and failures; setup failure is not product RED. Before the pilot the owner sets sample and thresholds for independent correct choices, time to first verifiable step, unnecessary steps and recommendation cancellations.
  - **PAOS-PMETH-22-AC04**: Use synthetic reproducible fixtures without providers/PII; select relevant cases per routing/prompt/contract change rather than repeatedly running everything.

- Verification gates: PV-EVAL; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Next step: Next dependency PAOS-PMETH-03.

#### Completion Report

- status: implemented
- what was done: Captured pre-policy baseline with outcomes, input hashes and the scenario matrix.
- files touched / work locations: [B1 evidence and canonical owners](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- technical value delivered: The owning route and its evidence are linked in the B1 record.
- product value delivered: A traceable read-only recommendation in the existing CLI.
- actual implementation date and time: 18-11-2026 20:43
- verification evidence: [B1 verification](../superpowers/specs/paos-pmeth-b1-evidence.en.md).
- residual risks: Web parity and actual-agent usefulness follow separate gates.
- follow-up: PAOS-PMETH-03.

### Task `PAOS-PMETH-23`

- Task: PAOS-PMETH-23
- Task name: Run end-to-end synthetic acceptance of the methodology path
- Status: implemented
- Priority: P1
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-26
- Blocks: PAOS-PMETH-24
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Prove a connected path using disposable user-project fixtures.
- Technical value: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Product value: Complete supported intent-to-evidence journeys.
- Scope: `tests/product_agent_os/`; `tests/web/single-window/`; `tests/fixtures/`; `docs/testing/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-23-AC01**: Repeat the read-only CLI/Web route on current source for the base profile. Meet the tasks and checks in profile_qualification for each claimed expansion, including staged plan, authorized fixture apply/build/check and evidence/verdict for writes, and override reload and stale verdict after AC changes for corresponding claims. Repeat PMETH-23 with the new scope and revision on expansion.
  - **PAOS-PMETH-23-AC02**: Verify journeys and states when Design is claimed. For claimed FSD coverage separately verify the migration proposal, selected incremental pilot and retention of sufficiently modular architecture. For claimed target apply verify PMETH-16 staged diff, compatibility, rollback and user-file preservation. Omit FSD gates for backend/CLI and keep AI quality as eval/gap without hidden provider calls.
  - **PAOS-PMETH-23-AC03**: Verify critical privacy/authority/user-file/isolation/false-ready cases, source/build/harness identity and cleanup for the claimed scope. A critical gap blocks the affected profile. Broad rollout exercises all branches and negatives, including real approval/recovery/rollback on a fixture.
  - **PAOS-PMETH-23-AC04**: Observe activation of API/runner intended paths in synthetic scope without old/fallback masking; model quality/human acceptance remain separate.

- Verification gates: PV-E2E; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + reviewer; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Next step: PAOS-PMETH-24

#### Completion Report

- status: implemented
- what was done: The base profile passed synthetic end-to-end acceptance, 35 browser checks and exact local revision qualification.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- technical value delivered: Verified in the approved B2 scope.
- product value delivered: An observable recommendation for a saved task.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- residual risks: The release remains on hold. Expanded profile and human comprehension need separate evidence.
- follow-up: PAOS-PMETH-24.

### Task `PAOS-PMETH-24`

- Task: PAOS-PMETH-24
- Task name: Evaluate usefulness with comparable actual-agent pilots
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-23
- Blocks: PAOS-PMETH-25
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Separate usefulness on actual tasks from deterministic-pipeline correctness.
- Technical value: Comparable outcome assessments with provenance and honest benefit verdicts.
- Product value: Understand usefulness on comparable tasks.
- Scope: `docs/product-agent-os/real-project-pilot.md`; `docs/testing/`; `docs/planning/user-project-methodologies-2026-11-15.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Comparable outcome assessments with provenance and honest benefit verdicts.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-24-AC01**: Run baseline/candidate on the same tasks/AC under comparable source/runtime/model conditions; record differences before comparison.
  - **PAOS-PMETH-24-AC02**: Use PMETH-22 thresholds to measure independent correct choices, time to first verifiable step, unnecessary steps, cancellations and reasons, accepted outcomes, defects/reopens, repair effort, owner interventions, elapsed and available token/cost. Mark missing measures unavailable.
  - **PAOS-PMETH-24-AC03**: Use separately authorized actual-agent/provider/real-project scope; without it retain bounded deterministic proof and insufficient_evidence for broad usefulness.
  - **PAOS-PMETH-24-AC04**: Report benefit/no-benefit/insufficient-evidence per project type and limits; retain failures without promoting broad readiness.

- Verification gates: PV-ACTUAL; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Comparable outcome assessments with provenance and honest benefit verdicts.
- Next step: PAOS-PMETH-25

#### Completion Report

- status: implemented
- what was done: Ran four matched Codex pairs on synthetic cases. Each arm had 4/4 correct first checks and verified outcomes.
- files touched / work locations: [PMETH-24 paired evaluation](../superpowers/specs/paos-pmeth-24-paired-evidence.en.md).
- technical value delivered: Preregistered cases, thresholds, time and token usage. A local verifier performed the checks Codex selected.
- product value delivered: One backend bug pair exceeded the timing threshold, with `insufficient_evidence` for the profile. The two docs-only cases returned `no_benefit`.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [Receipts for both series](../superpowers/specs/paos-pmeth-24-paired-receipts.json) · [Historical B2 pilot](../superpowers/specs/paos-pmeth-b2-evidence.en.md#usefulness-pilot).
- residual risks: Broad usefulness remains `insufficient_evidence`. Autonomous tool use, currency cost and real projects were outside the measurement. Delivery remains on `hold`.
- follow-up: PAOS-PMETH-25, owner decision about delivery.

### Task `PAOS-PMETH-25`

- Task: PAOS-PMETH-25
- Task name: Make a bounded delivery and rollout decision
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-24
- Blocks: None.
- External references: PAOS-FUNC-17
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Permit only evidence-backed bounded adoption.
- Technical value: Reviewable rollout/hold/rollback decisions without external actions.
- Product value: Receive only evidence-backed supported delivery options.
- Scope: `docs/product-agent-os/packaging-and-closure.md`; `docs/operations/`; `PLAN.md`; `RUNLOG.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Reviewable rollout/hold/rollback decisions without external actions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-25-AC01**: Record scope/revision, evidence and residual gaps in the owner-reviewed go/bounded_go/hold/no-go. Check status and evidence of the profile_qualification tasks for each claimed profile. Exclude unverified profiles and repeat profile-specific PMETH-23 before expansion. Update RU/EN guidance for confirmed paths only.
  - **PAOS-PMETH-25-AC02**: Document compatibility/update/rollback, disabling and preservation of user-authored target files; the decision performs no migration/install/distribution.
  - **PAOS-PMETH-25-AC03**: Assign owners/dispositions to provider-cost/privacy/licensing/host-activation gaps; wording cannot bypass missing necessary evidence.
  - **PAOS-PMETH-25-AC04**: Keep publication/active hooks/automation/new target permissions separate; internal A milestones do not gate product B.

- Verification gates: PV-DECISION; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: release-operator + product-manager; owner decision; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Reviewable rollout/hold/rollback decisions without external actions.
- Next step: Retain the approved release hold until new evidence is reviewed.

#### Completion Report

- status: implemented
- what was done: The owner approved a release hold for the qualified local revision. The disposition records scope, rollback and reevaluation gates.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- technical value delivered: Verified in the approved B2 scope.
- product value delivered: A recorded outcome for the owner’s rollout decision.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- residual risks: The release remains on hold. Expanded profile and human comprehension need separate evidence.
- follow-up: Apply the owner’s release hold.

### Task `PAOS-PMETH-26`

- Task: PAOS-PMETH-26
- Task name: Prepare user guidance and operator documentation
- Status: implemented
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: Spec-DD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-authorized B2 local implementation, synthetic acceptance and rollout disposition.
- Validator target: detailed task blocks
- Date and time of task implementation: 19-11-2026 11:10
- Depends on: PAOS-PMETH-20
- Blocks: PAOS-PMETH-23
- External references: PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Explain supported capabilities and safe actions without marketing claims.
- Technical value: RU/EN user/operator guides with source/command evidence.
- Product value: Understand available actions and product limits.
- Scope: `docs/product-agent-os/methodology-intelligence.md`; `docs/product-agent-os/operator-command-matrix.md`; `docs/operations/`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Verified RU/EN examples of the early CLI+Web path in existing guidance.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-26-AC01**: RU/EN guidance shows the verified early bug/docs CLI+Web path, inputs, reasons, scope, sources, next step and limits. Support examples with PMETH-22/19/20.
  - **PAOS-PMETH-26-AC02**: Explain the short route, intended RED versus setup failure, partial/unknown and a safe next action. Mark override/apply and Design/FSD as future until PMETH-23 and PMETH-25.
  - **PAOS-PMETH-26-AC03**: Distinguish current/staged/unsupported CLI/Web behavior; validate commands/links/source registry against implementation through TEST.
  - **PAOS-PMETH-26-AC04**: Reuse canonical guides/templates; screenshots/reports do not replace runtime evidence and metadata-only updates do not claim activation.

- Verification gates: PV-DOCS; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: docs-maintainer + product-manager; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Verified RU/EN examples of the early CLI+Web path in existing guidance.
- Next step: PAOS-PMETH-23

#### Completion Report

- status: implemented
- what was done: The canonical RU/EN guide contains checked CLI/Web examples, partial coverage and the safe next step.
- files touched / work locations: [B2 evidence and canonical route](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- technical value delivered: Verified in the approved B2 scope.
- product value delivered: An observable recommendation for a saved task.
- actual implementation date and time: 19-11-2026 11:10
- verification evidence: [B2 verification](../superpowers/specs/paos-pmeth-b2-evidence.en.md).
- residual risks: The release remains on hold. Expanded profile and human comprehension need separate evidence.
- follow-up: PAOS-PMETH-23.
