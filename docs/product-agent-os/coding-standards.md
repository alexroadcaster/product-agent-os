# Professional Code Authoring standards

Source status: `project-authored + research-backed + experiment`

Источники: Batch 45 research packets `plugins/product-agent-os/assets/research/ai-agent-coding-standards-research.md` и `plugins/product-agent-os/assets/research/ai-agent-coding-literature-research.md`, Batch 45 S5 packet `docs/superpowers/specs/batch45-professional-code-s5-learning-automation-summary.json`, S6 packets `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` и `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`, S7 packets `docs/superpowers/specs/batch45-real-project-scorecard.json` и `docs/superpowers/specs/batch45-real-project-decision-packet.json`, M37 remediation packet `docs/superpowers/specs/batch45-review-remediation-summary.json`, [Development Standards](development-standards.md), [Artifact Contracts](artifact-contracts.md), [Behavioral evals](behavioral-evals.md), [Scenarios](scenarios.md), [Code Review playbook](../playbooks/code-review.md).

Professional Code Authoring - это слой Product-Agent OS для не механических задач написания кода. Его цель проста: агент сначала ищет уже существующую возможность, стандартную библиотеку, фреймворк, конфигурацию или локальный helper, и только потом пишет новый код. Хороший результат может быть одной строкой, удалением лишнего кода или настройкой existing behavior, если это закрывает acceptance criteria с меньшим долгом.

## Что включается

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

Batch 45 currently supports `docs_contract_ready` / `synthetic_green` claims for local source artifacts, templates, eval cases, discovery/readiness visibility, runtime route visibility, generated HTML visibility and candidate-only learning-loop/automation policy. M26 records a live behavior-eval no-go, M27 keeps the M25 advisory local/non-blocking and rejects stronger advisory, CI and blocker promotion, M35 keeps S7 fixture-local/source-only with no-go for treatment v2 promotion, and M37 records local hook/validator hardening plus review remediation docs/control-plane sync only. T17 freezes the metadata-only held-out corpus manifest in `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json` / `B45-POSTQ4-T17-A01`; T18 defines the same-model promotion-grade eval design and strict schema in `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json` / `B45-POSTQ4-T18-A01`; T19 defines the cost/timeout/raw-temp-only retention policy in `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json` / `B45-POSTQ4-T19-A01`. They are not baseline/treatment runs, reviewer gates, provider/model calls or promotion decisions. They do not prove that AI agents now write enterprise-quality code in real projects; M26/M27/M35/M37/T17/T18/T19 only sharpen that ceiling.

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
