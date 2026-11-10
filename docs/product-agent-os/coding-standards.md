# Professional Code Authoring standards

Source status: `project-authored + research-backed + experiment`

Источники: Batch 45 research packets `plugins/product-agent-os/assets/research/ai-agent-coding-standards-research.md` и `plugins/product-agent-os/assets/research/ai-agent-coding-literature-research.md`, Batch 45 S5 packet `docs/superpowers/specs/batch45-professional-code-s5-learning-automation-summary.json`, S6 packets `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` и `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`, S7 packets `docs/superpowers/specs/batch45-real-project-scorecard.json` и `docs/superpowers/specs/batch45-real-project-decision-packet.json`, M37 remediation packet `docs/superpowers/specs/batch45-review-remediation-summary.json`, [Development Standards](development-standards.md), [Artifact Contracts](artifact-contracts.md), [Behavioral evals](behavioral-evals.md), [Scenarios](scenarios.md), [Code Review playbook](../playbooks/code-review.md).

Professional Code Authoring - это слой Product-Agent OS для не механических задач написания кода. Его цель проста: агент сначала ищет уже существующую возможность, стандартную библиотеку, фреймворк, конфигурацию или локальный helper, и только потом пишет новый код. Хороший результат может быть одной строкой, удалением лишнего кода или настройкой existing behavior, если это закрывает acceptance criteria с меньшим долгом.

## Ordinary authoring и текущая интеграция {#ordinary-authoring}

Для обычной правки default generation context — `.codex/artifact-templates/code-change-contract.md`: восемь полей T25, без повторного полного checklist. Активный workflow и packaged contract согласованы; `coding-standard-checklist.md` применяется как reviewer/reference material, когда нужны дополнительные детали.

Opt-in [ordinary CLI route](cli-reference.md#ordinary-route) связывает discovery с существующими selectors T26/T27. Каждая выбранная проверка должна иметь risk/invariant и source; отсутствие инструмента не разрешает auto-install. Docs-only может иметь `not_applicable`, а reuse/deletion/no-op — быть правильным результатом. Project-mandated checks сохраняются.

High-risk и full lifecycle reporting выбираются отдельно от длины coding contract. Локальные CLI/fixture проверки доказывают интеграцию; обновление активного файла не доказывает fresh-session loading. T23–T29 не переоткрываются, T30–T34 и behavioral promotion остаются отдельной очередью. Исторические Batch 45 receipts ниже сохраняют собственный evidence ceiling.

## Что включается

G7 уточняет локальные контракты: bounded capability summary приходит из текущего inventory в прежнее поле `existing_capability`; reference coverage остаётся unknown до чтения источников. Refactor использует существующие/characterization checks, без искусственного RED. Fingerprint включает известные lockfiles/config и явные `verification_paths`; `verification_environment` — сведения вызывающей стороны, не автоматическое доказательство версии инструмента. Missing coverage не означает clean.

Review различает доказанный дефект, предпочтение, отклонённое замечание и открытый риск; нужен checked revision и сценарий. T34 evaluator сохраняется byte-for-byte; G7 использует отдельный versioned evidence contract. Исследование и ограничения (`research/product-agent-os-g7-repository-deep-review-2026-11-09.md`), план G7 (`research/product-agent-os-audit-remediation-task-plan-2026-11-09.md`). Локальная проверка механизмов не доказывает улучшение модельной генерации или fresh-session loading.

| Gate | Что агент обязан записать | Когда можно пропустить |
| --- | --- | --- |
| `enterprise_leverage_check` | Какой existing path был проверен до custom implementation. | Mechanical docs/format-only edit с `not_applicable` reason. |
| `existing_capability_scan` | Standard library, framework, current dependency, project helper, config и deletion/reuse option. | Tiny isolated fix, если источник и причина очевидны и recorded. |
| `one_line_candidate` | Самое короткое прямое выражение или native call до multi-line helper. | Неприменимо для behavioral workflow, migration или UI composition. |
| `negative_dependency_rule` | Почему новая dependency нужна, какие alternatives rejected, rollback/removal path. | Нет новой dependency. |
| `deep_module_check` | Почему abstraction hides real complexity вместо shallow wrapper. | Direct call лучше abstraction. |
| `legacy_seam_check` | Characterization evidence, seam strategy, rollback или accepted gap. | Нет legacy/refactor impact. |
| `comment_policy` | Comments explain why, invariant, hazard или trade-off; state machines, algorithms, security/privacy/data/concurrency logic и функции с неочевидным invariant требуют docstring, intent comment или `comment_not_needed_reason`. | Код self-explanatory и comments не нужны; obvious comments запрещены как noise. |
| `cleverness_budget` | Payoff, tests, naming clarity и reviewer rationale. | Direct/simple path chosen. |

## Activation path

Product-Agent OS применяет этот стандарт через staged source artifacts:

| Surface | How it appears | Boundary |
| --- | --- | --- |
| Workflow | `.codex/workflows/coding-standards.md` из packaged template. | Template registration proves the workflow can be staged, not live enforcement. |
| Checklist | `.codex/artifact-templates/coding-standard-checklist.md`. | Review artifact; не source truth без текущего evidence. |
| Agent task packet | `.codex/artifact-templates/agent-task-packet.md` carries compact handoff fields. | Handoff contract, not raw research body. |
| Skills and agents | Builder/reviewer/architect/tester/docs-maintainer prompts reference the compact contract. | Skills activate by selection/context; they do not launch subagents automatically. |
| Evals | `behavioral-workflows.json`, agent-context contract and focused tests reject shortcut behavior. | Local deterministic coverage only. |
| Runtime route and HTML | `professional_code_authoring` appears as recommendation/visibility. | Generated view is `orientation_only_not_proof`. |

## Learning-loop improvement policy

Self-Learning Loop может предлагать будущие Professional Code Authoring improvements только как review candidates. Источники кандидатов - aggregate metrics, owner feedback, eval failures и manual pilot evidence; raw private chat bodies и hidden telemetry запрещены.

Кандидат может указывать только staged update targets: coding standards workflow, coding-standard checklist, behavioral/agent-context evals, hook-governance candidate docs и learning-loop/automation-promoter skill guidance. До review на promotion он должен иметь `minimum_manual_successful_runs: 3`, owner review, rollback/disable path, false-positive audit, flake replay и cost check.

До отдельного approval-gated batch Product-Agent OS не должен auto-apply такие candidates, activate hooks, create schedules, change global config, call providers, mutate target projects, ingest raw private chat или выполнять external writes.

## Senior leverage ladder

Use this order before writing new code:

1. Delete or avoid the code path entirely.
2. Use language construct, standard library or framework primitive.
3. Reuse current dependency or project helper already accepted by the repo.
4. Configure existing behavior instead of adding logic.
5. Compose a small direct expression.
6. Add a deep module only when it hides real complexity behind a stable interface.
7. Add dependency only after alternatives, lifecycle risk, security and removal path are recorded.

## Evidence ceiling

Batch 45 currently supports `docs_contract_ready` / `synthetic_green` claims for local source artifacts, templates, eval cases, discovery/readiness visibility, runtime route visibility, generated HTML visibility and candidate-only learning-loop/automation policy. M26 records a live behavior-eval no-go, M27 keeps the M25 advisory local/non-blocking and rejects stronger advisory, CI and blocker promotion, M35 keeps S7 fixture-local/source-only with no-go for treatment v2 promotion, and M37 records local hook/validator hardening plus review remediation docs/control-plane sync only. T17 freezes the metadata-only held-out corpus manifest in `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json` / `B45-POSTQ4-T17-A01`; T18 defines the same-model promotion-grade eval design and strict schema in `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json` / `B45-POSTQ4-T18-A01`; T19 defines the cost/timeout/raw-temp-only retention policy in `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json` / `B45-POSTQ4-T19-A01`; T20 stages historical exact approval packets in `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json` / `B45-POSTQ4-T20-A01` and `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json` / `B45-POSTQ4-T20-A02`, then records the consumed cost-waived approval in `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json` / `B45-POSTQ4-T20-A03`; T21 records blocked preflight history in `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json` / `B45-POSTQ4-T21-PREFLIGHT-A01`, `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json` / `B45-POSTQ4-T21-PREFLIGHT-A02` and `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json` / `B45-POSTQ4-T21-PREFLIGHT-A03`, plus current strict-schema abort evidence in `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json` / `B45-POSTQ4-T21-COST-WAIVED-RUN-A01` with `approved_primary_calls_started=1`, `reviewer_calls_started=0`, `valid_pair_count=0`, `invalid_pair_count=8` and `schema_failure_count=1`; T22 records a blocked reviewer/no-go decision in `docs/superpowers/specs/batch45-postq4-t22-promotion-grade-decision-packet.json` / `B45-POSTQ4-T22-A02` with `reviewer_gate_status=not_run_due_t21_invalid_schema_abort` and `promotion_allowed=false`. They are not valid baseline/treatment pair evidence, reviewer-gate evidence or promotion evidence. They do not prove that AI agents now write enterprise-quality code in real projects; M26/M27/M35/M37/T17/T18/T19/T20/T21/T22 only sharpen that ceiling.

Unsupported without a later approval-gated batch:

- live runtime or browser behavior;
- hook activation or blocking enforcement;
- active automation, schedule creation or Self-Learning Loop auto-apply;
- provider/model/API calls;
- installed plugin cache refresh;
- target workspace mutation;
- git, release, deploy or publish action;
- replacement of human review.

## Quick checklist

Before a non-mechanical code edit, the agent should be able to answer:

- What existing capability was checked?
- What is the one-line/native candidate?
- Why is custom code still needed?
- What dependency or legacy debt is added, avoided or removed?
- What test/eval/runtime evidence will support the claim?
- Which claims remain unsupported?

Next artifact: use [Development Standards](development-standards.md) to decide whether the gate applies, [Artifact Contracts](artifact-contracts.md) to inspect the checklist boundary and [Behavioral evals](behavioral-evals.md) to verify shortcut resistance.

## Архитектурные evidence G7

Разрешённый локальный корпус Import Linter 2.16 и dependency-cruiser 18.6.0 проверяет allowed, direct/transitive и cyclic dependencies; для JavaScript добавлены alias и unresolved-import controls. Код завершения JSON-процесса сам по себе не означает clean. Опциональный API профиля сверяет переданные актуальные receipts и неизменяемый baseline; обычный discovery остаётся declaration-only. Корпус `.mjs` не доказывает TypeScript resolver/type-only behavior. Результаты проверок (`research/product-agent-os-g7-execution-report-2026-11-09.md`).

Итог T08: сохраняются локальные G7 механизмы в проверенных границах. В принятом владельцем T07 сравнении baseline и treatment прошли по 6/6; превосходство и эффект отдельных компонентов не установлены. Design/results (`docs/superpowers/specs/paos-aud-g7-attested-results.json`) фиксируют generation-only scope, хеши и все попытки. Это не отменяет T34 no-go и не доказывает fresh-session activation. Владелец принял T06 и итоговое решение T08 10.11.2026; локальная группа G7 закрыта.
