# Batch 45 S9-C: test and deterministic metric repair

Source status: `locally implemented and focused-verified after bounded repair; no live/provider/runtime-activation evidence`

## Scope

- Schema version: task_matrix_plan_v1
- Generated: 14-08-2026 17:00 Europe/Moscow
- Project: Product-Agent OS
- Profile: test-debt reduction and deterministic code-quality metrics
- Timezone: Europe/Moscow

### Task `B45-S9-C`

- Task: implement `B45-CQRR-T28`, then `B45-CQRR-T29` in strict sequence.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: the user explicitly authorized implementation of `B45.S9-C` with agents and skills after local closure of `B45-S9-B`.
- Validator target: detailed task blocks
- Date and time of task implementation: 17-08-2026 06:06
- Depends on: locally verified `B45-CQRR-T24` and `B45-CQRR-T27`; T29 also depends on the green T28 handoff.
- Blocks: `B45-S9-D` and T30/T31 until the green T29 handoff.
- Source: `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json`; `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json`; current Batch 45 tests, promotion contracts and eval templates.
- Short description: replace repeated packet-specific exact assertions with generic schema/registry/traceability and parameterized invariants while preserving fault detection, then add pure deterministic quality-metric aggregation without model self-score promotion.
- Technical value: separates cold historical packet validation from active behavioral contracts and makes missing evidence, regression, mutation, benchmark applicability, churn, dependency and cost/latency signals explicit typed inputs.
- Product value: Product-Agent OS can compare change quality through reproducible local evidence without brittle test ceremony or trust in model self-assessment.
- Scope: T28 baseline inventory and three assigned test files; T29 `code_quality_metrics.py`, `code-quality-metrics.json` and focused metric test; independent local review; A06 docs/control-plane sync.
- Non-goals: T30-T34; historical packet or evidence-ID rewrite; live/provider/model/external reviewer calls; CLI/runtime activation; benchmark/CI/browser execution; target mutation; dependency installation; hooks/automation; Git/release/deploy/publication; any claim of improved model-generated code quality.
- Expected result: repeated historical exact-value assertion families are reduced by at least 50 percent or have source-owned exceptions, while seeded corruptions and runtime-contract mutations still fail; deterministic aggregation blocks on missing evidence, excludes diagnostic self-scores from promotion and keeps reviewer verdict separate.
- Acceptance criteria: T28 records the current baseline, proves equivalent fault detection and does not use a LOC ratio as a gate; T29 cannot promote from one warning/coverage/size/self-score proxy, cannot convert missing to zero/success and requires a current benchmark only for performance-applicable changes.
- Verification gates: red-before-green at agreed public seams; T28 before/after LOC and assertion-family inventory; seeded-corruption and active-contract suites; T29 metric calculation, aggregation, missing-evidence, mutation/regression and performance applicability cases; relevant full unittest route; JSON parse; independent reviewer and completion-skeptic; RU/EN task validators; docs tests; `python tools\check_docs.py`; `git diff --check`.
- Risks / approval gates: stop on lost fault detection, changed historical IDs, shared-test collision, T29 starting before the T28 gate, self-score/single-proxy promotion, missing-as-success, T30 reviewer logic mixed into T29 or any external action.
- Complexity: high
- Estimated execution time: 4-6 hours
- Agents: `architect` freezes T28/T29 seams and metric semantics; `tester` owns T28 and T29 RED tests in sequential windows; `plugin-runtime-builder` writes only the T29 module/schema; `reviewer` and `completion-skeptic` are read-only; `docs-maintainer` synchronizes A06 after the gate.
- Skills: `implementation-planner`; `agent-team-designer`; `tdd`; `python-design-patterns`; `python-code-style`; project-local docs and control-plane sync.
- Output artifacts: T28 test inventory/refactor and `test_batch45_packet_contracts.py`; T29 `code_quality_metrics.py`, `code-quality-metrics.json`, `test_batch45_code_quality_metrics.py`; A06 evidence sync.
- Next step: T28/T29 are locally accepted as A06; the next dependency route is T30, without provider/model/reviewer execution or a promotion claim.

#### Completion Report

- status: implemented
- what was done: the failed additive T28 attempt was repaired: legacy T18-T22 assertions and the 196-record manifest were replaced by semantic packet cases; deterministic metrics and promotion-contract integration were then implemented.
- files touched / work locations: `tests/product_agent_os/test_batch45_packet_contracts.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; lifecycle/control-plane projections.
- technical value delivered: repeated-family anomaly 196→34, combined test LOC 8130→5658, retained exceptions=3; missing evidence now blocks deterministic promotion and self-score is diagnostic only.
- product value delivered: test ceremony is reduced without losing seeded-fault detection; the quality decision is reproducible.
- actual implementation date and time: 17-08-2026 06:33
- verification evidence: T28 48/48; T29/promotion 23/23; the JSON metric template parsed in focused tests.
- residual risks: T30-T34, live behavior, independent external reviewer and runtime activation remain unverified.
- follow-up: `locally_implemented_focused_verified`; proceed to T30 only under its separate gate.

## Sequential ownership model

| Stage | Writing owner | Write scope | Handoff gate |
| --- | --- | --- | --- |
| T28 baseline and RED/GREEN | `tester` | only the three assigned test files | fault-detection equivalence and >=50% reduction/exception inventory |
| T28 review | none | read-only | Reviewer and Completion Skeptic authorize T29 |
| T29 architecture | none | read-only decision | frozen public metric schema and promotion invariants |
| T29 RED | `tester` | only the focused metric test | one behavioral tracer per cycle |
| T29 GREEN | `plugin-runtime-builder` | metric module and JSON template | pure deterministic aggregation green |
| Review/docs | read-only reviewers, then `docs-maintainer` | evidence-owned docs only | supported claims and residual risks |

## Methodology applicability

- Acceptance scenarios: exact behavior mappings are fixed in task acceptance and public-seam tests.
- Business/Product gates: `not_applicable`; product hypothesis and release measurement do not change.
- Domain model: applicable only as a local evidence schema; no runtime bounded context is created.
- FSD/frontend/backend readiness: `not_applicable`; UI, service runtime and deployment topology do not change.
- AI/RAG/live eval: `approval_required` and out of scope; local metrics do not prove model behavior.
- Docs tooling: existing unittest/check_docs; no install and no generated-site freshness claim.
