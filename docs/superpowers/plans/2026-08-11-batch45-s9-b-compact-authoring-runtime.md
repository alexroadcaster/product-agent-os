---
title: "Архив — Batch 45 S9-B: компактный authoring runtime"
---

# Архив — Batch 45 S9-B: компактный authoring runtime {#batch-45-s9-b-authoring-runtime}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `активный план локальной реализации; без live/provider/runtime-activation доказательств`

## Область

- Schema version: task_matrix_plan_v1
- Сформировано: 11-08-2026 16:09 Europe/Moscow
- Проект: Product-Agent OS
- Профиль: compact code-change contract, project-native selector и risk-based quality strategy
- Часовой пояс: Europe/Moscow

### Task `B45-S9-B`

- Task: реализовать `B45-CQRR-T25`, `B45-CQRR-T26` и `B45-CQRR-T27` строго последовательно.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: пользователь явно авторизовал реализацию группы `B45.S9-B` с агентами и skills после локального закрытия `B45-S9-A`.
- Validator target: detailed task blocks
- Date and time of task implementation: 14-08-2026 16:32
- Depends on: `B45-CQRR-A03`; локально verified `B45-CQRR-A04`; `B45-CQRR-T23` для T25.
- Blocks: `B45-S9-C` и T28 до зелёного T27 handoff.
- Source: `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json`; `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json`; текущие templates, discovery helpers и tests.
- Short description: заменить normal generation-time checklist injection компактным максимум-восьмиполейным contract, затем добавить pure stack/tool selector и минимальный risk-to-test/comment/performance selector.
- Technical value: отделяет decision-bearing pre-edit context от reference checklist, сохраняет detection как `present_unverified` и связывает каждое предлагаемое evidence-действие с конкретным риском или `not_applicable` причиной.
- Product value: Product-Agent OS сможет давать короткие проектно-нативные authoring-рекомендации без универсальной церемонии, установки инструментов или ложных quality claims.
- Scope: T25 templates, узкая registration entry в `templates.py` и focused test; T26 `code_quality_selector.py`, profile template и sequential shared behavior test; T27 `test_strategy_selector.py`, quality-strategy template и тот же test после T26 handoff; current-evidence docs/control-plane sync.
- Non-goals: T28-T34; live/provider/model/external reviewer calls; target mutation; dependency installation; browser/E2E/benchmark/CI execution; hook, automation, MCP или Agents SDK activation; Git/release/deploy/publication; claim об улучшении model-generated code quality.
- Expected result: default generation context использует decision-bearing contract не более восьми полей; selector покрывает Python, JS/TS, Go/Rust и Java/C# families и маркирует найденные tools `present_unverified`; strategy selector выбирает минимальный применимый набор evidence с named-risk rationale.
- Acceptance criteria: T25 не дублирует 128-line checklist и имеет explicit compatibility path и context-size evidence; T26 не устанавливает tools, не выдумывает thresholds и отличает detection от verification; T27 не форсирует TDD/E2E/mutation/coverage/benchmark и требует reason для selection или `not_applicable`.
- Verification gates: red-before-green focused tests на согласованных public seams; `python -m unittest tests.product_agent_os.test_batch45_coding_standards -v`; `python -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v`; template/artifact regressions; RU/EN task validators; JSON parse; `python tools\check_docs.py`; `git diff --check`; independent review и completion claim gate.
- Risks / approval gates: остановиться при более чем восьми contract fields, repackaged checklist, неявной compatibility, detection-as-verified, universal threshold, forced test layer, shared-test collision, scope expansion или внешнем действии.
- Complexity: high
- Estimated execution time: 90-150 minutes
- Agents: `architect` замораживает T25/T26/T27 semantics; `plugin-runtime-builder` пишет owned templates/modules; `tester` владеет focused tests в последовательных окнах; `reviewer` и `completion-skeptic` read-only; `docs-maintainer` синхронизирует evidence после gate.
- Skills: `implementation-planner`; `agent-team-designer`; `python-design-patterns`; `python-code-style`; `tdd`; project-local docs и control-plane sync.
- Output artifacts: `code-change-contract.md`; обновлённые `coding-standards.md` и `coding-standard-checklist.md`; canonical registration в `templates.py`; `code_quality_selector.py`; `code-quality-profile.md`; `test_strategy_selector.py`; обновлённый `quality-strategy.md`; focused T25 test; shared T26/T27 behavior test; A05 evidence sync.
- Next step: T28 в `B45-S9-C` после отдельного Task Brief; T28-T34 не начаты, а T34 требует нового exact approval.

#### Completion Report

- status: implemented
- what was done: последовательно реализованы T25 compact code-change contract с explicit compatibility, T26 pure stack/tool selector с `present_unverified` detection и T27 минимальный risk-to-test/comment/performance selector.
- files touched / work locations: T25 templates и `templates.py`; T26 `code_quality_selector.py` и profile template; T27 `test_strategy_selector.py`, quality-strategy template и focused tests.
- technical value delivered: normal generation context отделён от reference checklist; project-native detection и risk-selected evidence остаются детерминированными и не требуют установки tools.
- product value delivered: доступны короткие проектно-нативные authoring-рекомендации без универсальной церемонии и неподтверждённых quality claims.
- actual implementation date and time: 14-08-2026 16:32
- verification evidence: RED behavior `Ran 10, failures=3`; RED standards `Ran 6, failures=1`; final combined T25/T26/T27 command 54 OK exit 0 (focused 16/16, legacy 38/38); lifecycle/infrastructure integration 117/117; reviewer probe и reviewer `GO_local_code_gate`; completion-skeptic `GO_local_code_gate`; RU/EN task-matrix validators and JSON parse OK; docs 100/100, `python tools\check_docs.py` and `git diff --check` exit 0.
- residual risks: T28-T34 и все live/provider/promotion/readiness claims остаются вне scope.
- follow-up: начать T28 только отдельным маршрутом `B45-S9-C`; T29-T34 и все live/provider/promotion/readiness claims остаются вне scope.

## Последовательная ownership-модель

| Этап | Пишущий владелец | Write scope | Handoff gate |
| --- | --- | --- | --- |
| T25 architecture | нет | read-only решение | максимум восемь полей, explicit compatibility |
| T25 templates | `plugin-runtime-builder` | три T25 template path и только canonical registration entry в `templates.py` | template diff перед tester |
| T25 tests | `tester` | `test_batch45_coding_standards.py` | red/green, size и default-context evidence |
| T26 implementation | `plugin-runtime-builder` | selector и profile | pure detection API перед tester |
| T26 tests | `tester` | shared behavior test | four-family green и no-install proof |
| T27 implementation | `plugin-runtime-builder` | strategy selector/template | risk semantics перед tester |
| T27 tests | `tester` | shared behavior test после T26 release | positive/negative applicability green |
| Review/docs | read-only reviewers, затем `docs-maintainer` | evidence-owned docs only | supported claims и residual risks |

## Methodology applicability

- Acceptance scenarios: equivalent behavior mapping в task acceptance и focused tests; отдельный generated scenario artifact не нужен, потому что source packets уже фиксируют requirement -> check -> evidence owner.
- Business/Product gates: `not_applicable`; slice не меняет product hypothesis, analytics или release measurement.
- Domain model: `not_applicable`; локальные pure selectors не создают новый bounded context.
- FSD/frontend/backend readiness: `not_applicable`; UI, service runtime и deployment topology не меняются.
- AI/RAG/live eval: `approval_required` и вне scope; локальные selectors не доказывают model behavior.
- Docs tooling: existing unittest/check_docs; no install. The RU S9-B plan is classified as pending root-site freshness in `DOC_M25_PENDING_SITE_PAGES`; no MkDocs rebuild or generated-site freshness claim follows.
