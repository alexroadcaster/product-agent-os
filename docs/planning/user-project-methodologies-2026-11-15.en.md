# Product-Agent OS — direction B: methodologies for user projects

Source status: repository_source / owner_requested_planning / proposed_product_capability; implementation_not_started.
Date: 2026-11-15. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Purpose and two independent directions

**A — Product-Agent OS internal quality:** [internal plan](methodology-improvement-2026-11-15.en.md), [JSON](methodology-improvement-2026-11-15.json): 17 executable planned tasks with existing IDs retained; METH-16 is retained separately as a reference-only record.

**B — this product plan:** 26 new planned PAOS-PMETH-01–26 tasks extend selection, application and verification of Spec-Driven Development (Spec-DD), Design-Driven Development (Design-DD), Test-Driven Development (TDD), Agentic-Driven Development (ADD) and Feature-Sliced Design (FSD) in user projects. [JSON](user-project-methodologies-2026-11-15.json) owns status/priority/dependencies; [Russian](user-project-methodologies-2026-11-15.md) contains matching detailed cards.

B does not depend on A's internal dashboard/tasks/workflows FSD migration, METH-18 go decisions or completion of all FUNC groups. Shared files require coordinated ownership/sequential writes rather than invented functional dependencies. Planning authorizes no implementation: all timestamps remain pending_execution_timestamp; active skills/workflows/hooks/config, targets, runtime/providers, installation, Git and publication are unchanged by this request.

## Existing implementation and remaining evidence

Source snapshot: git HEAD `5a9c87bea374accc953a8401fa1ac32678ff6e6e`; JSON records 15 source-owner hashes. This is source inspection, not a new runtime/model/browser acceptance run. The initial FUNC owner snapshot had 10 implemented / 24 planned after G01/G02. Concurrent FUNC-G03 started during planning; its live task-state and later source edits belong to that workstream and are not frozen by this matrix. These are not fresh runtime receipts; future slices require current source reads.

| Area | Source observation | New task responsibility |
| --- | --- | --- |
| Discovery/intake | discovery.py calls build_methodology_audit; task_routing.py has explicit context and file-free intake | PMETH-01/02 verify the path and retain intent/provenance without another scanner |
| Catalog/audit/synthesis | Twelve domains, recommendations, readiness states and grouped safe next actions already exist | PMETH-03/04 refine five-method decisions, compatibility and proportionality |
| Runner/skills | routes.py builds methodology_packet; contracts/guards and lifecycle/requirements/test-eval skills exist | PMETH-05–17 connect decisions to artifacts/execution/evidence instead of recreating roles |
| CLI entrypoints | run_methodology_audit.py accepts workspace plus JSON/report; other entrypoints expose task intake | PMETH-01/02 select canonical adapters; an empty-intent default does not mean all engine paths lose intent |
| Infrastructure | Dry-run/stage/manifest/approval-aware merge and rollback exist | PMETH-12/16 reuse and verify that pipeline rather than another writer |
| Web/local service | Inspection did not establish a direct methodology-specific owner in searched Web/local-service/contracts keyword scopes | PMETH-01 establishes reuse/bridge/gaps and PMETH-18–21 connect the chosen path; negative keyword search does not prove complete absence |
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

| Group | Tasks | Outcome and gate |
| --- | --- | --- |
| B0. Decisions and baseline | 01–04, 22 | Confirmed owners, profiles, policy/contracts and predefined scenario outcomes |
| B1. Spec/Design/TDD | 05–09 | Connected contracts/states/checks without unnecessary gates |
| B2. Target frontend FSD | 10–12 | Suitability → source boundaries → reversible staged migration |
| B3. ADD and delivery | 13–17 | Skills/ownership → one DAG → safe stage/apply → criterion evidence; CLI core checkpoint |
| B4. Web/desktop | 18–21 | Durable state → observed API bridge → clear UI → recovery/audit |
| B5. Acceptance/delivery | 23, 24, 26, 25 | Synthetic E2E → actual-agent usefulness; docs → bounded rollout decision |

Start PMETH-01 → 02 → 22 → 03 → 04, then DAG-independent Spec/Design/TDD, FSD and ADD branches, with one writer per shared file. PMETH-15 combines them; PMETH-16/17 provide a core checkpoint without Web prerequisites. B4 does not gate CLI-only work in a target project. PMETH-23 verifies the selected complete CLI/Web path, PMETH-24 isolates model usefulness and PMETH-25 decides adoption. JSON contains 54 dependency edges; task numbers are not execution order.

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

## Verification of this planning revision

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
| PAOS-PMETH-01 | P1 | B0; Spec-DD, ADD | Audit the existing methodology path and assign owners | — |
| PAOS-PMETH-02 | P1 | B0; Spec-DD, ADD | Normalize project profiles and user intent | PAOS-PMETH-01 |
| PAOS-PMETH-03 | P1 | B0; Spec-DD, Design-DD, TDD, ADD, FSD | Select proportionate methodologies and explain decisions | PAOS-PMETH-02, PAOS-PMETH-22 |
| PAOS-PMETH-04 | P1 | B0; Spec-DD, ADD | Define a versioned methodology contract | PAOS-PMETH-03 |
| PAOS-PMETH-05 | P1 | B1; Spec-DD | Integrate a Spec-Driven route from intent to verifiable specification | PAOS-PMETH-04, PAOS-PMETH-22 |
| PAOS-PMETH-06 | P1 | B1; Spec-DD, ADD | Track specification changes and stale context | PAOS-PMETH-05 |
| PAOS-PMETH-07 | P1 | B1; TDD, Spec-DD | Integrate TDD and bug reproduction into slice execution | PAOS-PMETH-05, PAOS-PMETH-22 |
| PAOS-PMETH-08 | P1 | B1; Design-DD, Spec-DD | Integrate Design-Driven journeys and state matrices | PAOS-PMETH-05, PAOS-PMETH-22 |
| PAOS-PMETH-09 | P1 | B1; Design-DD, TDD | Verify UI against the accepted design contract | PAOS-PMETH-07, PAOS-PMETH-08 |
| PAOS-PMETH-10 | P1 | B2; FSD, Spec-DD | Determine FSD applicability and propose architecture choices | PAOS-PMETH-04, PAOS-PMETH-22 |
| PAOS-PMETH-11 | P1 | B2; FSD, TDD | Verify frontend dependencies from source | PAOS-PMETH-10 |
| PAOS-PMETH-12 | P2 | B2; FSD, Spec-DD | Create incremental FSD migration proposals for user projects | PAOS-PMETH-06, PAOS-PMETH-11 |
| PAOS-PMETH-13 | P1 | B3; ADD, Spec-DD | Integrate ADD execution and ownership contracts | PAOS-PMETH-04, PAOS-PMETH-22 |
| PAOS-PMETH-14 | P2 | B3; ADD | Connect methodology decisions to available skills and tools | PAOS-PMETH-13 |
| PAOS-PMETH-15 | P1 | B3; Spec-DD, Design-DD, TDD, ADD, FSD | Compose methodologies into one proportionate delivery plan | PAOS-PMETH-05, PAOS-PMETH-07, PAOS-PMETH-08, PAOS-PMETH-10, PAOS-PMETH-13 |
| PAOS-PMETH-16 | P1 | B3; Spec-DD, ADD, FSD | Integrate safe staging, previews and authorized application | PAOS-PMETH-06, PAOS-PMETH-12, PAOS-PMETH-14, PAOS-PMETH-15 |
| PAOS-PMETH-17 | P1 | B3; Spec-DD, TDD, Design-DD, ADD, FSD | Collect evidence and compute criterion-based readiness | PAOS-PMETH-09, PAOS-PMETH-11, PAOS-PMETH-13, PAOS-PMETH-16 |
| PAOS-PMETH-18 | P2 | B4; Spec-DD, ADD | Define durable methodology state in Web/desktop | PAOS-PMETH-04, PAOS-PMETH-15, PAOS-PMETH-17 |
| PAOS-PMETH-19 | P2 | B4; ADD, Spec-DD | Connect the Python methodology engine to application API/runtime | PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-18 |
| PAOS-PMETH-20 | P2 | B4; Design-DD, Spec-DD | Expose methodology choices, plans and evidence in the UI | PAOS-PMETH-19 |
| PAOS-PMETH-21 | P1 | B4; ADD, Spec-DD | Handle drift, stopping, resumption and audit | PAOS-PMETH-17, PAOS-PMETH-19, PAOS-PMETH-20 |
| PAOS-PMETH-22 | P1 | B0; Spec-DD, Design-DD, TDD, ADD, FSD | Prepare user-project baseline and acceptance eval matrices | PAOS-PMETH-01, PAOS-PMETH-02 |
| PAOS-PMETH-23 | P1 | B5; Spec-DD, Design-DD, TDD, ADD, FSD | Run end-to-end synthetic acceptance of the methodology path | PAOS-PMETH-17, PAOS-PMETH-21, PAOS-PMETH-22 |
| PAOS-PMETH-24 | P2 | B5; ADD, Spec-DD | Evaluate usefulness with comparable actual-agent pilots | PAOS-PMETH-23 |
| PAOS-PMETH-25 | P2 | B5; ADD, Spec-DD | Make a bounded delivery and rollout decision | PAOS-PMETH-24, PAOS-PMETH-26 |
| PAOS-PMETH-26 | P2 | B5; Spec-DD, Design-DD | Prepare user guidance and operator documentation | PAOS-PMETH-20, PAOS-PMETH-23 |

## Detailed direction B task cards

### Task `PAOS-PMETH-01`

- Task: PAOS-PMETH-01
- Task name: Audit the existing methodology path and assign owners
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B0
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: None.
- Blocks: PAOS-PMETH-02, PAOS-PMETH-22
- External references: PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Audit and extend existing components instead of building a parallel methodology engine.
- Technical value: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Product value: Avoid rebuilding working components.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-01-AC01**: Map reuse/extend/missing from discovery to audit/catalog/synthesis, task routing, runner/skills, stage/merge and Web; substantiate each edge with source.
  - **PAOS-PMETH-01-AC02**: Separate readiness/detection, staged proposals and execution; a missing Web keyword is not proof of missing integration.
  - **PAOS-PMETH-01-AC03**: Choose one owner and an existing entrypoint for every new contract; do not create a duplicate engine.
  - **PAOS-PMETH-01-AC04**: List baseline fixtures, commands, revision and compatibility consumers; the audit does not change active target assets.

- Verification gates: PV-PLAN; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + explorer; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Existing-component, gap and canonical-owner map in PMETH-01 evidence.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-02`

- Task: PAOS-PMETH-02
- Task name: Normalize project profiles and user intent
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B0
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-01
- Blocks: PAOS-PMETH-03, PAOS-PMETH-22
- External references: PAOS-FUNC-28
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Provide minimal reliable context for choosing process depth.
- Technical value: Normalized profile/intent receipts with provenance and compatibility tests.
- Product value: Receive a process appropriate to the task and environment.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/question_protocol.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Normalized profile/intent receipts with provenance and compatibility tests.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-02-AC01**: Distinguish greenfield/legacy, surface, scale/coupling, risk, change mode, available checks and environment limits; repository size is not risk.
  - **PAOS-PMETH-02-AC02**: Pass actual intent/AC to audit/route; preserve file-free intake and task_context while explicitly rejecting mixed/malformed inputs.
  - **PAOS-PMETH-02-AC03**: Give facts provenance/revision and separate assumptions/missing context; a material blocking question does not replace available reads.
  - **PAOS-PMETH-02-AC04**: Docs-only, small bugfix and backend-only work do not receive full product ceremony or frontend gates.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Normalized profile/intent receipts with provenance and compatibility tests.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-03`

- Task: PAOS-PMETH-03
- Task name: Select proportionate methodologies and explain decisions
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B0
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-02, PAOS-PMETH-22
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
  - **PAOS-PMETH-03-AC03**: Missing evidence produces a question/gap/present_unverified rather than a violation or present_verified; record override reasons without relaxing permissions/invariants.
  - **PAOS-PMETH-03-AC04**: PMETH-22 baseline/candidate cases show no blanket FSD/DDD/TDD mandate, hidden new gates or false readiness.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Explainable decisions for five methodologies and baseline/candidate routing evidence.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-04`

- Task: PAOS-PMETH-04
- Task name: Define a versioned methodology contract
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B0
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-03
- Blocks: PAOS-PMETH-05, PAOS-PMETH-10, PAOS-PMETH-13, PAOS-PMETH-18
- External references: PAOS-FUNC-08
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Maintain one compatible contract across engine, runner and UI.
- Technical value: Canonical versioned contracts, adapters and compatibility tests.
- Product value: Keep CLI/runner/Web decisions consistent.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_catalog.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `packages/contracts/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Canonical versioned contracts, adapters and compatibility tests.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-04-AC01**: Choose one canonical schema owner and Python/TypeScript adapters; validate decision/profile, project/task identity, revisions and evidence references.
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
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-05`

- Task: PAOS-PMETH-05
- Task name: Integrate a Spec-Driven route from intent to verifiable specification
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-04, PAOS-PMETH-22
- Blocks: PAOS-PMETH-06, PAOS-PMETH-07, PAOS-PMETH-08, PAOS-PMETH-15
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Turn user intent into a verifiable contract for the selected slice.
- Technical value: Concise/full requirements proposals with AC traceability and assigned ownership.
- Product value: Accept outcomes against clear criteria.
- Scope: `plugins/product-agent-os/skills/requirements-author/SKILL.md`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Concise/full requirements proposals with AC traceability and assigned ownership.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-05-AC01**: Use concise scope/AC in an existing owner for small work and requirements/non-goals/invariants/scenarios for complex work; create no empty mandatory document.
  - **PAOS-PMETH-05-AC02**: Link every AC to an observable scenario/check/evidence owner or explicit gap; expose ambiguity/assumptions before build.
  - **PAOS-PMETH-05-AC03**: Extend user-authored requirements through staged proposals/diffs without overwriting or creating another source of truth.
  - **PAOS-PMETH-05-AC04**: Do not scaffold greenfield work before selecting the first vertical slice and obtaining applicable authority; specification changes are not working-code proof.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + product-manager; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Concise/full requirements proposals with AC traceability and assigned ownership.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-06`

- Task: PAOS-PMETH-06
- Task name: Track specification changes and stale context
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-05
- Blocks: PAOS-PMETH-12, PAOS-PMETH-16
- External references: PAOS-FUNC-02, PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Prevent stale-plan execution and retain requirement/evidence consistency.
- Technical value: Revision/impact/disposition records and stale-context regression evidence.
- Product value: Preserve decisions and avoid stale instructions.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/product_agent_os/control_plane_documents.py`; `plugins/product-agent-os/scripts/product_agent_os/documentation_sync.py`. Future work locations; PMETH-01 refines exact owned files before execution.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-07`

- Task: PAOS-PMETH-07
- Task name: Integrate TDD and bug reproduction into slice execution
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-05, PAOS-PMETH-22
- Blocks: PAOS-PMETH-09, PAOS-PMETH-15
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Apply test-first where it validates behavior and explain exceptions honestly.
- Technical value: Test/eval routes, RED/GREEN receipts and justified exceptions.
- Product value: Receive reproducible fixes and regression protection.
- Scope: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/scripts/product_agent_os/test_strategy_selector.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/assets/templates/workflows/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Test/eval routes, RED/GREEN receipts and justified exceptions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-07-AC01**: For changed testable behavior require observable RED for the intended reason, minimal GREEN and scoped refactor; record command, revision and expected/actual in existing evidence.
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
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-08`

- Task: PAOS-PMETH-08
- Task name: Integrate Design-Driven journeys and state matrices
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-05, PAOS-PMETH-22
- Blocks: PAOS-PMETH-09, PAOS-PMETH-15
- External references: UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Design journeys and states before implementing changed user interactions.
- Technical value: Journey/state matrices, design references and acceptance boundaries.
- Product value: Check usability before expensive implementation.
- Scope: `plugins/product-agent-os/assets/templates/artifact-templates/`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/skills/requirements-author/SKILL.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Journey/state matrices, design references and acceptance boundaries.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-08-AC01**: Define the user goal, steps, data, interaction/error/empty/loading/dirty states and accessibility for changed journeys; backend-only work gets not_applicable.
  - **PAOS-PMETH-08-AC02**: Reuse existing design/system and propose missing states separately; a new mockup is not user-approved by default.
  - **PAOS-PMETH-08-AC03**: Distinguish synthetic/current/unavailable data and real API constraints; do not promise unsupported states as available functions.
  - **PAOS-PMETH-08-AC04**: Separate design, implementation and human-acceptance ownership/evidence; small UI changes do not require full-project redesign.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Journey/state matrices, design references and acceptance boundaries.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-09`

- Task: PAOS-PMETH-09
- Task name: Verify UI against the accepted design contract
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B1
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-07, PAOS-PMETH-08
- Blocks: PAOS-PMETH-17
- External references: PAOS-FUNC-19, UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Compare the running interface against accepted design contracts.
- Technical value: Current-build visual/interaction evidence or explicit unavailable gaps.
- Product value: See design-versus-runtime differences.
- Scope: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`; `plugins/product-agent-os/assets/templates/artifact-templates/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Current-build visual/interaction evidence or explicit unavailable gaps.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-09-AC01**: Select available component/browser/visual/keyboard checks for the changed journey, viewport/theme/long-content states and source/build/harness provenance.
  - **PAOS-PMETH-09-AC02**: Check composition/actions beyond overflow/contrast; detect intentional fixture mismatch and make baseline updates reviewable.
  - **PAOS-PMETH-09-AC03**: Screenshot/prototype passes are not human-usability acceptance, WCAG certification or API-side-effect proof.
  - **PAOS-PMETH-09-AC04**: If runtime/browser is unavailable or unauthorized, return a gap and safe next action without bypassing limits or substituting old screenshots.

- Verification gates: PV-DESIGN; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Current-build visual/interaction evidence or explicit unavailable gaps.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-10`

- Task: PAOS-PMETH-10
- Task name: Determine FSD applicability and propose architecture choices
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B2
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-04, PAOS-PMETH-22
- Blocks: PAOS-PMETH-11, PAOS-PMETH-15
- External references: PAOS-FUNC-30
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Recommend FSD only with evidence of usefulness for the user frontend.
- Technical value: FSD applicability decisions and architecture proposals with alternatives.
- Product value: Choose architecture based on usefulness rather than fashion.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/assets/methodology/methodology-catalog.json`; `plugins/product-agent-os/assets/templates/artifact-templates/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: FSD applicability decisions and architecture proposals with alternatives.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-10-AC01**: Produce evidence-based distinct recommendations for small/static frontends, backend/native-only work, growing frontends and already-modular legacy.
  - **PAOS-PMETH-10-AC02**: Compare preserving architecture, strengthening boundaries and gradual FSD using coupling, change frequency, ownership and migration cost.
  - **PAOS-PMETH-10-AC03**: Propose only useful layers/slices/public APIs; whole-screen folders are not automatically features and backend/Python do not receive frontend FSD.
  - **PAOS-PMETH-10-AC04**: An architecture proposal requires an applicable owner decision before migration; absence of FSD is not itself a defect.

- Verification gates: PV-ENGINE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: FSD applicability decisions and architecture proposals with alternatives.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-11`

- Task: PAOS-PMETH-11
- Task name: Verify frontend dependencies from source
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B2
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-10
- Blocks: PAOS-PMETH-12, PAOS-PMETH-17
- External references: PAOS-FUNC-30
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Separate folder signals from verified code boundaries for supported languages.
- Technical value: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Product value: Receive verifiable architecture findings.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/project_code_graph.py`; `tests/product_agent_os/test_methodology_audit.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-11-AC01**: Bind supported JS/TS/TSX import/public-API checks to source revisions; do not silently skip aliases/reexports/type/literal dynamic imports.
  - **PAOS-PMETH-11-AC02**: Unsupported syntax/aliases/symlinks/out-of-scope sources produce partial/unknown coverage; graphs/folder names do not establish present_verified.
  - **PAOS-PMETH-11-AC03**: Report path/line/rule/owner for violations and distinguish valid entity public APIs and legacy exceptions.
  - **PAOS-PMETH-11-AC04**: Pass RED/GREEN parser/boundary and no-source-mutation checks; reuse current parsers/adapters and the F30 decision without mandatory installation.

- Verification gates: PV-FSD; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Source-bound findings, coverage/unknown reports and boundary regression cases.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-12`

- Task: PAOS-PMETH-12
- Task name: Create incremental FSD migration proposals for user projects
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B2
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-06, PAOS-PMETH-11
- Blocks: PAOS-PMETH-16
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Plan minimal reversible migration under accepted boundaries.
- Technical value: Incremental migration plans with pilots/public APIs/rollback and staged diffs.
- Product value: Improve frontend structure incrementally without behavior loss.
- Scope: `plugins/product-agent-os/skills/implementation-planner/SKILL.md`; `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/assets/templates/artifact-templates/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Incremental migration plans with pilots/public APIs/rollback and staged diffs.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-12-AC01**: Include baseline imports, a minimal pilot, AC, owners, dependencies, compatibility bridges and rollback; no mandatory full rewrite.
  - **PAOS-PMETH-12-AC02**: Define public APIs/import ratchet before selected shared/entities and one screen; gate expansion on accepted checkpoints.
  - **PAOS-PMETH-12-AC03**: Preserve existing architecture/user files/dirty changes; moved code retains business/API semantics and new code does not import legacy internals.
  - **PAOS-PMETH-12-AC04**: Read-only scanning writes reports/proposals only to authorized staging; target apply and hook activation require their own authority.

- Verification gates: PV-STAGE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: architect + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Incremental migration plans with pilots/public APIs/rollback and staged diffs.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-13`

- Task: PAOS-PMETH-13
- Task name: Integrate ADD execution and ownership contracts
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-04, PAOS-PMETH-22
- Blocks: PAOS-PMETH-14, PAOS-PMETH-15, PAOS-PMETH-17
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-14`

- Task: PAOS-PMETH-14
- Task name: Connect methodology decisions to available skills and tools
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B3
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-13
- Blocks: PAOS-PMETH-16
- External references: PAOS-FUNC-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Connect decisions to available executors without hidden installation.
- Technical value: Skill/tool routes with provenance, capabilities and safe fallback dispositions.
- Product value: Use available capabilities without hidden environment changes.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/skills/references/`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`. Future work locations; PMETH-01 refines exact owned files before execution.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-15`

- Task: PAOS-PMETH-15
- Task name: Compose methodologies into one proportionate delivery plan
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-05, PAOS-PMETH-07, PAOS-PMETH-08, PAOS-PMETH-10, PAOS-PMETH-13
- Blocks: PAOS-PMETH-16, PAOS-PMETH-18
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Produce one delivery DAG with the minimum necessary gates.
- Technical value: A single delivery DAG linking methods to each slice.
- Product value: Use one consistent plan rather than competing queues.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `plugins/product-agent-os/skills/implementation-planner/SKILL.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: A single delivery DAG linking methods to each slice.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-15-AC01**: Use one DAG for requirements/design/architecture/test/build/review; resolve artifact aliases to canonical owners rather than five independent queues.
  - **PAOS-PMETH-15-AC02**: Use actual contract prerequisites; small bugfixes do not wait for a full PRD, every control-plane document, team setup or FSD migration.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-16`

- Task: PAOS-PMETH-16
- Task name: Integrate safe staging, previews and authorized application
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Spec-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-06, PAOS-PMETH-12, PAOS-PMETH-14, PAOS-PMETH-15
- Blocks: PAOS-PMETH-17, PAOS-PMETH-19
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Use the existing approval-aware pipeline without losing user-authored files.
- Technical value: Stage/preview/approval/apply/rollback receipts for fixture targets.
- Product value: Preserve authored files and control proposal application.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/stage_manifest.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/merge_infrastructure.py`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Stage/preview/approval/apply/rollback receipts for fixture targets.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-16-AC01**: Reuse dry-run/stage/manifest/merge; keep staging outside the target and perform no target writes without applicable exact authority.
  - **PAOS-PMETH-16-AC02**: Preview owned paths, user-file handling, method/AC links and side effects; do not overwrite existing unmarked AGENTS/config/hooks.
  - **PAOS-PMETH-16-AC03**: Reject drift, wrong root/project, traversal/symlinks and stale approvals; preserve user changes during partial-apply recovery.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-17`

- Task: PAOS-PMETH-17
- Task name: Collect evidence and compute criterion-based readiness
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B3
- Methodologies: Spec-DD, TDD, Design-DD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-09, PAOS-PMETH-11, PAOS-PMETH-13, PAOS-PMETH-16
- Blocks: PAOS-PMETH-18, PAOS-PMETH-19, PAOS-PMETH-21, PAOS-PMETH-23
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Support readiness for every applicable check with current evidence.
- Technical value: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Product value: Distinguish evidence-backed outcomes from plans and assumptions.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_synthesis.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-17-AC01**: Link requirement → scenario → check → receipt → verdict with owners, revision/environment and applicability; accepted gaps are not passed checks.
  - **PAOS-PMETH-17-AC02**: Detection/generated files/test counts/report formatting cannot independently promote readiness; keep missing/stale/failed receipts visible.
  - **PAOS-PMETH-17-AC03**: Use runtime evidence for implementation/provider-path claims when required and authorized; unit smoke is not activation.
  - **PAOS-PMETH-17-AC04**: The CLI core pilot links applicable methods/checks on one fixture revision; separate technical, human and release acceptance.

- Verification gates: PV-EVIDENCE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Criterion/evidence/readiness ledgers separating technical/human/release outcomes.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-18`

- Task: PAOS-PMETH-18
- Task name: Define durable methodology state in Web/desktop
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-04, PAOS-PMETH-15, PAOS-PMETH-17
- Blocks: PAOS-PMETH-19
- External references: PAOS-FUNC-08, PAOS-FUNC-22
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Persist consistent project/task state without a second status authority.
- Technical value: Durable profile/decision/evidence models and synthetic migration/recovery checks.
- Product value: Resume with consistent project/task state.
- Scope: `packages/contracts/`; `apps/local-service/src/storage/`; `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/artifacts/service.mts`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Durable profile/decision/evidence models and synthetic migration/recovery checks.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-18-AC01**: Define project/task scope and canonical profile/decision/plan/evidence owners; SQLite and imported MD/JSON do not become competing status authorities.
  - **PAOS-PMETH-18-AC02**: Support version/revision/CAS, history, project isolation and explicit unknowns; older clients/newer schemas do not lose data.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-19`

- Task: PAOS-PMETH-19
- Task name: Connect the Python methodology engine to application API/runtime
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-18
- Blocks: PAOS-PMETH-20, PAOS-PMETH-21
- External references: PAOS-FUNC-01, PAOS-FUNC-08
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Connect the existing methodology engine to an observable application path.
- Technical value: Versioned bridge/API and current-path activation/negative receipts.
- Product value: Use an observable methodology path in the application.
- Scope: `apps/local-service/src/http/application.mts`; `apps/local-service/src/runtime/`; `packages/contracts/`; `plugins/product-agent-os/scripts/product_agent_os/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Versioned bridge/API and current-path activation/negative receipts.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-19-AC01**: Use the PMETH-01 selected bridge and versioned contract; verify HTTP/Python/runner parity through actual adapters rather than mock-only echoes.
  - **PAOS-PMETH-19-AC02**: Separate read-only recommendations from authorized apply; negatively test session/origin/CSRF/project scope/input bounds/cancellation.
  - **PAOS-PMETH-19-AC03**: Expose the intended path/selector in diagnostic receipts; prevent old paths/fallbacks masking the scenario and disallow silent bridge fallback.
  - **PAOS-PMETH-19-AC04**: The bridge calls no model/provider, runs no arbitrary repo command and uses no real credentials; pinned-source changes follow TEST qualification.

- Verification gates: PV-BRIDGE; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: builder — local-service + plugin-runtime-builder; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Versioned bridge/API and current-path activation/negative receipts.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-20`

- Task: PAOS-PMETH-20
- Task name: Expose methodology choices, plans and evidence in the UI
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B4
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-19
- Blocks: PAOS-PMETH-21, PAOS-PMETH-26
- External references: PAOS-FUNC-24, UI-12
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Help users understand choices, limitations and next actions.
- Technical value: Approved UI flows, selected-scope implementation and browser evidence.
- Product value: Understand next actions, limits and stopping reasons.
- Scope: `apps/web/src/ui/App.tsx`; `apps/web/src/features/tasks/`; `apps/web/src/features/projects/`; `apps/web/src/locales/`; `docs/frontend/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Approved UI flows, selected-scope implementation and browser evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-20-AC01**: Agree placement in existing project/task flows, prototype and states before build; explain why a method applies, its required/optional/not-applicable status and the next step.
  - **PAOS-PMETH-20-AC02**: Show source/coverage/unknown, scope/diffs/permissions and stop reasons; choosing advice does not look like apply or a successful build.
  - **PAOS-PMETH-20-AC03**: Provide loading/empty/error/stale/conflict/permission-required states, RU/EN, themes and keyboard/focus; backend unavailability is not fixture success.
  - **PAOS-PMETH-20-AC04**: A synthetic browser journey uses the PMETH-19 API; preserve manual overrides/dispositions/audit without requiring internal FSD migration.

- Verification gates: PV-UI; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + builder — web; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Approved UI flows, selected-scope implementation and browser evidence.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-21`

- Task: PAOS-PMETH-21
- Task name: Handle drift, stopping, resumption and audit
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B4
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-17, PAOS-PMETH-19, PAOS-PMETH-20
- Blocks: PAOS-PMETH-23
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
  - **PAOS-PMETH-21-AC03**: Audit minimal decisions/receipts/reasons with redaction, ownership and time; retain partial/failed attempts after later success.
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

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-22`

- Task: PAOS-PMETH-22
- Task name: Prepare user-project baseline and acceptance eval matrices
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B0
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-01, PAOS-PMETH-02
- Blocks: PAOS-PMETH-03, PAOS-PMETH-05, PAOS-PMETH-07, PAOS-PMETH-08, PAOS-PMETH-10, PAOS-PMETH-13, PAOS-PMETH-23
- External references: None; internal A is not a prerequisite.
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Define expected behavior and baselines before changing routing.
- Technical value: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Product value: Receive routing checked on ordinary and negative cases.
- Scope: `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_methodology_synthesis.py`; `tests/product_agent_os/test_codex_runtime_runner_fixture_eval.py`; `plugins/product-agent-os/assets/fixtures/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-22-AC01**: Cover tiny CLI/docs-only, backend/API bugs, greenfield frontend, coupled legacy, already-bounded frontend, native and AI/RAG; specify methods/depth/gaps before candidates.
  - **PAOS-PMETH-22-AC02**: Include misleading folders, unknown aliases, stale specs, forged success, missing tests, prompt injection, dirty user files, denied writes, wrong project/revision and unavailable tools.
  - **PAOS-PMETH-22-AC03**: Retain actual baseline results/known failures; do not pass expected future capabilities before implementation or treat setup failure as product RED.
  - **PAOS-PMETH-22-AC04**: Use synthetic reproducible fixtures without providers/PII; select relevant cases per routing/prompt/contract change rather than repeatedly running everything.

- Verification gates: PV-EVAL; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Synthetic scenario matrices, expected outcomes and preserved baseline ledgers.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-23`

- Task: PAOS-PMETH-23
- Task name: Run end-to-end synthetic acceptance of the methodology path
- Status: planned
- Priority: P1
- Direction: B — user projects
- Delivery group: B5
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-17, PAOS-PMETH-21, PAOS-PMETH-22
- Blocks: PAOS-PMETH-24, PAOS-PMETH-26
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Prove a connected path using disposable user-project fixtures.
- Technical value: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Product value: Complete supported intent-to-evidence journeys.
- Scope: `tests/product_agent_os/`; `tests/web/single-window/`; `tests/fixtures/`; `docs/testing/`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-23-AC01**: On current sources verify read-only scan → reasoned selection → staged plan → authorized fixture apply/build/check → evidence/verdict for applicable PMETH-22 scenarios.
  - **PAOS-PMETH-23-AC02**: Frontend pilots demonstrate incremental FSD/design states; backend/CLI receive no FSD and AI quality stays eval/gap without hidden provider calls.
  - **PAOS-PMETH-23-AC03**: Pass all critical privacy/authority/user-file/isolation/false-readiness negatives; verify source/build/harness hashes and cleanup, with critical unresolved gaps blocking closure.
  - **PAOS-PMETH-23-AC04**: Observe activation of API/runner intended paths in synthetic scope without old/fallback masking; model quality/human acceptance remain separate.

- Verification gates: PV-E2E; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: tester + reviewer; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: End-to-end receipt matrices for supported scenarios and findings dispositions.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-24`

- Task: PAOS-PMETH-24
- Task name: Evaluate usefulness with comparable actual-agent pilots
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B5
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
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
  - **PAOS-PMETH-24-AC02**: Measure accepted outcomes, defects/reopens, repair effort, owner interventions, elapsed and available token/cost data; invent no zeros or productivity percentages.
  - **PAOS-PMETH-24-AC03**: Use separately authorized actual-agent/provider/real-project scope; without it retain bounded deterministic proof and insufficient_evidence for broad usefulness.
  - **PAOS-PMETH-24-AC04**: Report benefit/no-benefit/insufficient-evidence per project type and limits; retain failures without promoting broad readiness.

- Verification gates: PV-ACTUAL; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: L
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: product-manager + tester; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: Comparable outcome assessments with provenance and honest benefit verdicts.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-25`

- Task: PAOS-PMETH-25
- Task name: Make a bounded delivery and rollout decision
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B5
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-24, PAOS-PMETH-26
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

  - **PAOS-PMETH-25-AC01**: Bind owner-reviewed go/bounded_go/hold/no-go to supported project types/gates/evidence without promising autonomous production delivery.
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
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.

### Task `PAOS-PMETH-26`

- Task: PAOS-PMETH-26
- Task name: Prepare user guidance and operator documentation
- Status: planned
- Priority: P2
- Direction: B — user projects
- Delivery group: B5
- Methodologies: Spec-DD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested user-project methodology capability plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-PMETH-20, PAOS-PMETH-23
- Blocks: PAOS-PMETH-25
- External references: PAOS-FUNC-25
- Source: [source snapshot and state owner](user-project-methodologies-2026-11-15.json); existing components above and canonical paths below.
- Short description: Explain supported capabilities and safe actions without marketing claims.
- Technical value: RU/EN user/operator guides with source/command evidence.
- Product value: Understand available actions and product limits.
- Scope: `docs/product-agent-os/methodology-intelligence.md`; `docs/product-agent-os/operator-command-matrix.md`; `docs/operations/`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Future work locations; PMETH-01 refines exact owned files before execution.
- Non-goals: Duplicate existing engines/owners, implement internal A or unrelated FUNC/M5; current authoring authorizes no code, target/provider/Git/publication.
- Expected result: RU/EN user/operator guides with source/command evidence.
- Acceptance criteria: Four observable criteria below; missing evidence is not a pass.

  - **PAOS-PMETH-26-AC01**: RU/EN guidance explains inputs, selection, next artifacts/actions, checks, permissions, gaps and stopping through confirmed PMETH-22/PMETH-23 examples.
  - **PAOS-PMETH-26-AC02**: Explain small-task shortcuts, legacy/FSD opt-in, design acceptance and TDD failures without guaranteeing project success.
  - **PAOS-PMETH-26-AC03**: Distinguish current/staged/unsupported CLI/Web behavior; validate commands/links/source registry against implementation through TEST.
  - **PAOS-PMETH-26-AC04**: Reuse canonical guides/templates; screenshots/reports do not replace runtime evidence and metadata-only updates do not claim activation.

- Verification gates: PV-DOCS; profile above plus current TEST affected-contract routing; future checks were not executed during planning.
- Risks / approval gates: Apply common authority/data/stop boundaries; production/real-project/provider/install/activation need applicable authority. Durable prompt/routing changes require baseline/candidate evals before promotion.
- Complexity: M
- Estimated execution time: Estimate after PMETH-01 and bounded-slice discovery; no invented estimate/calendar commitment.
- Agents: docs-maintainer + product-manager; proposed ownership; delegation=0 now, future concurrency follows actual boundaries.
- Skills: Reuse canonical project skills listed in Scope; future Python uses python-design-patterns/python-code-style and UI uses frontend-testing-debugging. Skill presence does not prove invocation.
- Output artifacts: RU/EN user/operator guides with source/command evidence.
- Next step: Check dependencies and source/authority freshness, then select a separately authorized bounded slice.

#### Completion Report

- status: planned
- what was done: Task card authored; implementation not started.
- files touched / work locations: This authoring changed no implementation files; future locations appear in Scope.
- technical value delivered: Not claimed before executing AC.
- product value delivered: Not claimed before executing AC.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Static authoring/split checks only; future AC are not executed.
- residual risks: Baselines may change; applicability/authority/activation and model usefulness require selected-slice evidence.
- follow-up: Next authorized slice from the DAG, without automatic execution.
