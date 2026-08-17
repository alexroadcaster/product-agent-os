# Batch 45 S9-B: compact authoring runtime

Source status: `active local implementation plan; no live/provider/runtime-activation evidence`

## Scope

- Schema version: task_matrix_plan_v1
- Generated: 11-08-2026 16:09 Europe/Moscow
- Project: Product-Agent OS
- Profile: compact code-change contract, project-native selector and risk-based quality strategy
- Timezone: Europe/Moscow

### Task `B45-S9-B`

- Task: implement `B45-CQRR-T25`, `B45-CQRR-T26` and `B45-CQRR-T27` in strict sequence.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: the user explicitly authorized implementation of `B45.S9-B` with agents and skills after local closure of `B45-S9-A`.
- Validator target: detailed task blocks
- Date and time of task implementation: 14-08-2026 16:32
- Depends on: `B45-CQRR-A03`; locally verified `B45-CQRR-A04`; `B45-CQRR-T23` for T25.
- Blocks: `B45-S9-C` and T28 until the T27 green handoff.
- Source: `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json`; `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json`; current templates, discovery helpers and tests.
- Short description: replace normal generation-time checklist injection with a compact maximum-eight-field contract, then add a pure stack/tool selector and a minimum risk-to-test/comment/performance selector.
- Technical value: separates decision-bearing pre-edit context from the reference checklist, preserves detection as `present_unverified`, and ties every proposed evidence action to a concrete risk or `not_applicable` reason.
- Product value: Product-Agent OS can provide short project-native authoring guidance without universal ceremony, tool installation, or unsupported quality claims.
- Scope: T25 templates, one narrow registration entry in `templates.py` and focused test; T26 `code_quality_selector.py`, profile template and sequential shared behavior test; T27 `test_strategy_selector.py`, quality-strategy template and the same test after T26 handoff; current-evidence docs/control-plane sync.
- Non-goals: T28-T34; live/provider/model/external reviewer calls; target mutation; dependency installation; browser/E2E/benchmark/CI execution; hook, automation, MCP or Agents SDK activation; Git/release/deploy/publication; any claim of improved model-generated code quality.
- Expected result: default generation context uses a decision-bearing contract of at most eight fields; the selector covers Python, JS/TS, Go/Rust and Java/C# families and labels detected tools `present_unverified`; the strategy selector chooses the minimum applicable evidence set with named-risk rationale.
- Acceptance criteria: T25 does not duplicate the 128-line checklist and has an explicit compatibility path and context-size evidence; T26 does not install tools, invent thresholds or confuse detection with verification; T27 does not force TDD/E2E/mutation/coverage/benchmark and requires a reason for every selection or `not_applicable` outcome.
- Verification gates: red-before-green focused tests at agreed public seams; `python -m unittest tests.product_agent_os.test_batch45_coding_standards -v`; `python -m unittest tests.product_agent_os.test_batch45_code_quality_behavior -v`; template/artifact regressions; RU/EN task validators; JSON parse; `python tools\check_docs.py`; `git diff --check`; independent review and completion claim gate.
- Risks / approval gates: stop on more than eight contract fields, a repackaged checklist, unclear compatibility, detection-as-verified, universal thresholds, forced test layers, shared-test collision, scope expansion or any external action.
- Complexity: high
- Estimated execution time: 90-150 minutes
- Agents: `architect` freezes T25/T26/T27 semantics; `plugin-runtime-builder` writes owned templates/modules; `tester` owns focused tests in sequential windows; `reviewer` and `completion-skeptic` are read-only; `docs-maintainer` synchronizes evidence after the gate.
- Skills: `implementation-planner`; `agent-team-designer`; `python-design-patterns`; `python-code-style`; `tdd`; project-local docs and control-plane sync.
- Output artifacts: `code-change-contract.md`; updated `coding-standards.md` and `coding-standard-checklist.md`; canonical registration in `templates.py`; `code_quality_selector.py`; `code-quality-profile.md`; `test_strategy_selector.py`; updated `quality-strategy.md`; focused T25 test; shared T26/T27 behavior test; A05 evidence sync.
- Next step: T28 in `B45-S9-C` after a separate Task Brief; T28-T34 are not started and T34 requires a new exact approval.

#### Completion Report

- status: implemented
- what was done: sequentially implemented T25 compact code-change contract with explicit compatibility, T26 pure stack/tool selector with `present_unverified` detection, and T27 minimum risk-to-test/comment/performance selector.
- files touched / work locations: T25 templates and `templates.py`; T26 `code_quality_selector.py` and profile template; T27 `test_strategy_selector.py`, quality-strategy template and focused tests.
- technical value delivered: normal generation context is separated from the reference checklist; project-native detection and risk-selected evidence stay deterministic and require no tool installation.
- product value delivered: short project-native authoring recommendations are available without universal ceremony or unsupported quality claims.
- actual implementation date and time: 14-08-2026 16:32
- verification evidence: RED behavior `Ran 10, failures=3`; RED standards `Ran 6, failures=1`; final combined T25/T26/T27 command 54 OK exit 0 (focused 16/16, legacy 38/38); lifecycle/infrastructure integration 117/117; reviewer probe and reviewer `GO_local_code_gate`; completion-skeptic `GO_local_code_gate`; RU/EN task-matrix validators and JSON parse OK; docs 100/100, `python tools\check_docs.py` and `git diff --check` exit 0.
- residual risks: T28-T34 and all live/provider/promotion/readiness claims remain out of scope.
- follow-up: start T28 only through the separate `B45-S9-C` route; T29-T34 and all live/provider/promotion/readiness claims remain out of scope.

## Sequential ownership model

| Stage | Writing owner | Write scope | Handoff gate |
| --- | --- | --- | --- |
| T25 architecture | none | read-only decision | at most eight fields, explicit compatibility |
| T25 templates | `plugin-runtime-builder` | three T25 template paths and only the canonical registration entry in `templates.py` | template diff before tester |
| T25 tests | `tester` | `test_batch45_coding_standards.py` | red/green, size and default-context evidence |
| T26 implementation | `plugin-runtime-builder` | selector and profile | pure detection API before tester |
| T26 tests | `tester` | shared behavior test | four-family green and no-install proof |
| T27 implementation | `plugin-runtime-builder` | strategy selector/template | risk semantics before tester |
| T27 tests | `tester` | shared behavior test after T26 release | positive/negative applicability green |
| Review/docs | read-only reviewers, then `docs-maintainer` | evidence-owned docs only | supported claims and residual risks |

## Methodology applicability

- Acceptance scenarios: equivalent behavior mapping in task acceptance and focused tests; a separate generated scenario artifact is unnecessary because source packets already fix requirement -> check -> evidence owner.
- Business/Product gates: `not_applicable`; the slice does not change product hypothesis, analytics or release measurement.
- Domain model: `not_applicable`; local pure selectors do not create a new bounded context.
- FSD/frontend/backend readiness: `not_applicable`; no UI, service runtime or deployment topology changes.
- AI/RAG/live eval: `approval_required` and out of scope; local selectors do not prove model behavior.
- Docs tooling: existing unittest/check_docs; no install. The RU S9-B plan is classified as pending root-site freshness in `DOC_M25_PENDING_SITE_PAGES`; no MkDocs rebuild or generated-site freshness claim follows.
