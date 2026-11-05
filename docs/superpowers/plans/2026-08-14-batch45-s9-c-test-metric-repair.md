---
title: "Архив — Batch 45 S9-C: ремонт тестов и детерминированных метрик"
---

# Архив — Batch 45 S9-C: ремонт тестов и детерминированных метрик {#batch-45-s9-c}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `локально реализовано и focused-verified после bounded repair; без live/provider/runtime-activation доказательств`

## Область

- Schema version: task_matrix_plan_v1
- Сформировано: 14-08-2026 17:00 Europe/Moscow
- Проект: Product-Agent OS
- Профиль: сокращение test debt и deterministic code-quality metrics
- Часовой пояс: Europe/Moscow

### Task `B45-S9-C`

- Task: реализовать `B45-CQRR-T28`, затем `B45-CQRR-T29` строго последовательно.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: пользователь явно авторизовал реализацию группы `B45.S9-C` с агентами и skills после локального закрытия `B45-S9-B`.
- Validator target: detailed task blocks
- Date and time of task implementation: 17-08-2026 06:06
- Depends on: локально verified `B45-CQRR-T24` и `B45-CQRR-T27`; T29 дополнительно зависит от зелёного T28 handoff.
- Blocks: `B45-S9-D` и T30/T31 до зелёного T29 handoff.
- Source: `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json`; `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json`; текущие Batch 45 tests, promotion contracts и eval templates.
- Short description: заменить повторяющиеся packet-specific exact assertions generic schema/registry/traceability и parameterized invariants, сохранив fault detection, затем ввести pure deterministic quality-metric aggregation без model self-score promotion.
- Technical value: отделяет cold historical packet validation от active behavioral contracts и делает missing evidence, regression, mutation, benchmark applicability, churn, dependency и cost/latency сигналы явными типизированными входами.
- Product value: Product-Agent OS сможет сравнивать качество изменений по воспроизводимым локальным доказательствам без хрупкой тестовой церемонии и без доверия к самооценке модели.
- Scope: T28 baseline inventory и три назначенных test-файла; T29 `code_quality_metrics.py`, `code-quality-metrics.json` и focused metric test; независимый local review; A06 docs/control-plane sync.
- Non-goals: T30-T34; historical packet или evidence-ID rewrite; live/provider/model/external reviewer calls; CLI/runtime activation; benchmark/CI/browser execution; target mutation; dependency installation; hooks/automation; Git/release/deploy/publication; claim об улучшении model-generated code quality.
- Expected result: repeated historical exact-value assertion families сокращены минимум на 50 процентов либо имеют source-owned exception, seeded corruptions и runtime-contract mutations продолжают падать; deterministic aggregation блокируется на missing evidence, игнорирует diagnostic self-scores для promotion и отделяет reviewer verdict.
- Acceptance criteria: T28 записывает текущий baseline, доказывает equivalent fault detection и не использует LOC ratio как gate; T29 не разрешает promotion от одного warning/coverage/size/self-score proxy, не превращает missing в zero/success и требует current benchmark только для performance-applicable изменений.
- Verification gates: red-before-green на согласованных public seams; T28 before/after LOC и assertion-family inventory; seeded-corruption и active-contract suites; T29 metric calculation, aggregation, missing-evidence, mutation/regression и performance applicability cases; relevant full unittest route; JSON parse; independent reviewer и completion-skeptic; RU/EN task validators; docs tests; `python tools\check_docs.py`; `git diff --check`.
- Risks / approval gates: остановиться при утрате fault detection, изменении historical IDs, shared-test collision, запуске T29 до T28 gate, self-score/single-proxy promotion, missing-as-success, смешивании T30 reviewer logic или любом внешнем действии.
- Complexity: high
- Estimated execution time: 4-6 hours
- Agents: `architect` замораживает T28/T29 seams и metric semantics; `tester` владеет T28 и T29 RED tests в последовательных окнах; `plugin-runtime-builder` пишет только T29 module/schema; `reviewer` и `completion-skeptic` read-only; `docs-maintainer` синхронизирует A06 после gate.
- Skills: `implementation-planner`; `agent-team-designer`; `tdd`; `python-design-patterns`; `python-code-style`; project-local docs и control-plane sync.
- Output artifacts: T28 test inventory/refactor и `test_batch45_packet_contracts.py`; T29 `code_quality_metrics.py`, `code-quality-metrics.json`, `test_batch45_code_quality_metrics.py`; A06 evidence sync.
- Next step: T28/T29 локально приняты как A06; следующий dependency route — T30, без запуска provider/model/reviewer и без promotion claim.

#### Completion Report

- status: implemented
- what was done: неудачная additive попытка T28 была отремонтирована: legacy T18-T22 assertions и 196-record manifest заменены semantic packet cases; затем реализованы deterministic metrics и promotion-contract integration.
- files touched / work locations: `tests/product_agent_os/test_batch45_packet_contracts.py`; `tests/product_agent_os/test_coding_standards_artifacts.py`; `tests/product_agent_os/test_batch45_code_quality_behavior.py`; lifecycle/control-plane projections.
- technical value delivered: repeated-family anomaly 196→34, combined test LOC 8130→5658, retained exceptions=3; missing evidence now blocks deterministic promotion and self-score is diagnostic only.
- product value delivered: сокращена тестовая церемония без потери seeded-fault detection; quality decision стал воспроизводимым.
- actual implementation date and time: 17-08-2026 06:33
- verification evidence: T28 48/48; T29/promotion 23/23; JSON metric template parsed in focused test.
- residual risks: T30-T34, live behavior, independent external reviewer and runtime activation remain unverified.
- follow-up: `locally_implemented_focused_verified`; proceed to T30 only under its separate gate.

## Последовательная ownership-модель

| Этап | Пишущий владелец | Write scope | Handoff gate |
| --- | --- | --- | --- |
| T28 baseline и RED/GREEN | `tester` | только три назначенных test-файла | fault-detection equivalence и >=50% reduction/exception inventory |
| T28 review | нет | read-only | Reviewer и Completion Skeptic разрешают T29 |
| T29 architecture | нет | read-only решение | frozen public metric schema и promotion invariants |
| T29 RED | `tester` | только focused metric test | один behavioral tracer за цикл |
| T29 GREEN | `plugin-runtime-builder` | metric module и JSON template | pure deterministic aggregation green |
| Review/docs | read-only reviewers, затем `docs-maintainer` | evidence-owned docs only | supported claims и residual risks |

## Methodology applicability

- Acceptance scenarios: exact behavior mappings зафиксированы в task acceptance и public-seam tests.
- Business/Product gates: `not_applicable`; product hypothesis и release measurement не меняются.
- Domain model: применим только как локальный evidence schema; runtime bounded context не создаётся.
- FSD/frontend/backend readiness: `not_applicable`; UI, service runtime и deployment topology не меняются.
- AI/RAG/live eval: `approval_required` и вне scope; локальные metrics не доказывают model behavior.
- Docs tooling: existing unittest/check_docs; no install и no generated-site freshness claim.
