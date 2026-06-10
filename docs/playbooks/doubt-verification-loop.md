# Playbook: Doubt / verifier loop

Source status: `official + experiment`

Источники: [Grounded answering](grounded-answering.md), [Hallucination Control](../prompting/anti-hallucination.md), [Artifact Contracts](../product-agent-os/artifact-contracts.md), [Behavioral evals](../product-agent-os/behavioral-evals.md), [Batch 40 source-transfer packet](../sources/product-agent-os-batch40-doubt-verifier-source-transfer.md).

## Purpose

Doubt / verifier loop превращает ручной запрос "проверь еще раз" в проверяемый completion gate. Рабочая форма: `worker_output -> doubt_verification_packet -> completion-skeptic -> revise_or_pass`.

Цель не в том, чтобы агент нервно переписал ответ. Цель в том, чтобы извлечь проверяемые claims, требования, evidence gaps и approval boundaries, а затем изменить только те части, где verifier нашел подтвержденный дефект или missing evidence.

## Trigger

Используйте `completion-skeptic`, когда есть хотя бы один сигнал:

- пользователь просит "проверь еще раз", "мы ничего не забыли", "перед финалом проверь";
- агент собирается сказать "done", "ready", "works", "fixed", "verified" или эквивалент;
- изменен код, docs/source registry, архитектурный контракт, security/release/eval слой;
- ответ опирается на current facts, source-sensitive docs, tool output или generated views;
- есть риск false pass, false rewrite, stale evidence или approval bypass.

Не запускайте loop для простого deterministic вывода, если нет completion claim, risk class или user-trigger.

## Workflow

1. Сохранить artifact under review: worker output, diff summary, doc draft, plan row или final answer candidate.
2. Извлечь claim ledger: каждое проверяемое утверждение получает `claim_type`, `status`, `evidence_refs` и `residual_risk`.
3. Извлечь requirement ledger: user request, acceptance criteria, non-goals, approval constraints и missing context.
4. Заполнить evidence ledger: source registry, local files, current commands, eval runs, owner decisions, approved browser/runtime/web checks или explicit missing check.
5. Запустить skeptic pass: `completion-skeptic` возвращает verdict `pass | revise | needs_more_context | blocked_by_approval | accepted_risk`.
6. Reviser меняет только confirmed gaps. Rule: do not rewrite first.
7. Финальный ответ называет что проверено, что исправлено, что осталось accepted_gap или residual risk.

## Packet Excerpt

```yaml
doubt_verification_packet_v1:
  artifact_under_review: "final answer candidate"
  claim_ledger:
    - id: "C1"
      claim: "The docs navigation includes the new playbook."
      claim_type: "docs_behavior"
      status: "supported"
      evidence_refs: ["mkdocs_nav_current_run"]
  requirement_ledger:
    - id: "R1"
      requirement: "Document architecture, diagrams and examples."
      status: "covered"
  evidence_ledger:
    - id: "mkdocs_nav_current_run"
      provider: "current_command"
      provenance_kind: "command"
      status: "available"
  verdict:
    status: "revise"
    reason: "One example category is missing."
  accepted_gaps:
    - owner: "Product owner"
      reason: "Manual pilot evidence is B40-S5 scope."
      residual_risk: "Usefulness is not proven by docs alone."
      follow_up: "Run B40-S5 pilot ledger."
```

## Examples

| Example id | Task type | Trigger | Packet focus | Safe final style |
| --- | --- | --- | --- | --- |
| `docs_research_example` | docs/research answer | "Проверь источники" | source registry, official/community split, `needs_fresh_check` | Separate supported facts, assumptions and unsupported claims. |
| `code_check_example` | code change | "Готово?" | current command evidence, lint/test gaps, approval boundary | Name commands run and missing checks; avoid works claim without run evidence. |
| `architecture_review_example` | architecture/spec | "Ничего не упустили?" | requirements, non-goals, dependency and rollback gaps | Revise only confirmed architecture gaps. |
| `product_planning_example` | feature plan | "Проверь матрицу" | acceptance criteria, user value, dependencies, stop conditions | Return missing tasks and accepted scope cuts. |
| `security_release_example` | release/security | "Можно выпускать?" | approval gates, source status, rollback, no-unapproved-actions proof | Block or accepted_risk instead of release claim. |
| `ai_eval_example` | AI/eval work | "Проверь качество" | baseline, current eval, scorecard thresholds, false pass/rewrite | Keep manual-only until pilot and owner review. |

## Failure Modes

- False pass: packet says `pass` while evidence is stale, generated-only or approval-blocked.
- False rewrite: skeptic rewrites correct content without a confirmed gap.
- Fake evidence: command output, source IDs or tool traces are invented.
- Context leak: raw private chat logs, secrets or local absolute paths enter packet examples.
- Automation drift: manual success is skipped and the loop becomes an active hook, MCP server, Agents SDK runner or automation.

## Boundaries

No active hook, automation, MCP server, Agents SDK runner or provider call is created by this playbook. It documents the manual and plugin-local path only. Future guardrail or runtime integration requires a separate approval packet, privacy review, scorecard evidence and rollback/disable path.

## Next Artifact

For one task, produce a `doubt_verification_packet` and a short final answer update. For repeated success, record failure examples, eval cases and owner review, then consider the normal promotion chain: manual -> playbook -> skill -> plugin -> automation candidate.
