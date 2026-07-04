# B45-POSTQ4-T06-PROMOTION-DECISION source evidence

Source status: read-only analysis for Batch 45 T06. No runtime/provider/browser/target/git actions were run.

## Вывод

Рекомендованный decision state для T06: `keep_advisory_only_no_go_for_treatment_v2_promotion`.

Обоснование коротко: локальная static-дельта по Q4 стала нулевой по предупреждениям, но это не является promotion evidence. Единственный live rerun для T05 завершился `stopped_on_timeout_inconclusive_no_go`, treatment и reviewer comparison не были получены, а T05B лишь оформил новый approval packet без исполнения.

## 1) Evidence, которые поддерживают T06

- [`docs/superpowers/specs/batch45-post-q4-next-tasks.json`](../../../docs/superpowers/specs/batch45-post-q4-next-tasks.json)
  - T06 прямо запланирован как `decision_gate` после T03/T05/T05B.
  - В `execution_update.warning_delta` зафиксировано `q4_baseline_warning_count: 14`, `post_t03_warning_count: 0`, `delta: -14`, `blocking: false`.
  - В `status_by_task` T03 помечен как `implemented_local_static_delta_verify`, T05 как `stopped_on_timeout_inconclusive_no_go`, T05B как `implemented_approval_packet_only_not_run`.
  - В `t05_live_eval_result.decision` явно сказано `does_not_reverse_M26_or_M35_no_go`.

- [`docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json`](../../../docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json)
  - T01-T03 подтверждают только локальное static warning reduction.
  - `B45-POSTQ4-T03-STATIC-DELTA-VERIFY` показывает `q4_baseline_warning_count: 14`, `post_fix_warning_count: 0`, `warning_delta: -14`, `blocking: false`, `suppressed_warning_count: 0`.
  - `py_compile_status: passed` и `secret_pattern_matches: 0` поддерживают только hygiene/static quality, не promotion.

- [`docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`](../../../docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json)
  - Live attempt был approved, но остановлен на timeout: `status: stopped_on_timeout_inconclusive_no_go`.
  - `baseline_run.status: stopped_on_timeout_before_baseline_complete`, `treatment_run.status: not_run_due_baseline_timeout_stop_rule`.
  - `decision.state: no_go_stopped_on_timeout`, `promotion_allowed: false`, `static_warning_delta_can_promote: false`, `m26_reversed: false`, `m35_reversed: false`.
  - `unsupported_claims` explicitly excludes runtime/browser/provider/target/release readiness and real behavior improvement.

- [`docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`](../../../docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json)
  - Confirms T05B is `approval_packet_only_not_run`.
  - States default without new approval is `do_not_run; proceed only to no-go/promotion decision using existing evidence ceiling`.
  - `promotion_threshold` requires live comparable runs, which T05B does not provide.

- [`docs/superpowers/specs/batch45-agent-behavior-eval-results.json`](../../../docs/superpowers/specs/batch45-agent-behavior-eval-results.json)
  - Baseline/treatment live eval already ended in `no_go_real_behavior_improvement_not_proven_after_live_eval`.
  - Even where warnings improved, `average_local_score` dropped from `4.22` to `3.88`, `tasks_treatment_worse: 4`, and `timeout_runs: 1`.
  - This is the strongest source-owned evidence that promotion should not be inferred from static warning reduction alone.

- [`docs/superpowers/specs/batch45-real-project-decision-packet.json`](../../../docs/superpowers/specs/batch45-real-project-decision-packet.json)
  - Records the broader decision ceiling as `keep_advisory_only_no_go_for_treatment_v2_promotion`.
  - Explicitly rejects CI/blocker promotion and real AI-agent behavior improvement without runtime evidence.
  - Names runtime/browser/provider/data/release gaps as accepted only for no-go, not for promotion.

## 2) Evidence, которые НЕ поддерживают promotion

- Static warning reduction alone.
  - T03 reduced Q4 advisory warnings from 14 to 0, but the packet itself says `static_warning_delta_can_promote: false`.
  - Static cleanliness is useful, but it does not prove behavior improvement, rollback safety, or runtime parity.

- T05 live attempt.
  - The rerun did not produce a baseline-vs-treatment comparison.
  - Baseline timed out before completion, treatment did not run, reviewer did not run.
  - Therefore the live evidence cannot reverse `M26` or `M35` no-go states.

- T05B approval packet.
  - This is only a redesigned approval packet.
  - It contains no execution evidence, no runtime proof, no reviewer result, and no promotion delta.

- Existing broader no-go packets.
  - `B45-PCA-M26` already states `no_go_real_behavior_improvement_not_proven_after_live_eval`.
  - `B45-PCA-M35` states `keep_advisory_only_no_go_for_treatment_v2_promotion`.
  - Both are consistent with preserving no-go, not promoting.

## 3) Точная recommendation для T06 decision state

Recommended decision state:

`keep_advisory_only_no_go_for_treatment_v2_promotion`

Why this exact state:

- It matches the strongest source-owned decision packets.
- It preserves the distinction between static cleanup and real promotion evidence.
- It does not overstate T03 delta as behavioral proof.
- It does not treat T05B as execution evidence.

If a more granular state is required by the T06 schema, the closest equivalent is:

`no_go_preserve_advisory_only_static_delta_not_sufficient`

## 4) Open gaps

- No valid baseline-vs-treatment comparison from the live rerun.
- No treatment completion evidence for T05.
- No independent reviewer decision from the T05 rerun because the run stopped early.
- No runtime/browser/target evidence.
- No rollback/compatibility/CI promotion evidence.
- No source-owned evidence that static warning delta maps to real AI-agent behavior improvement.
- T05B needs exact new approval before any rerun; until then it is packet-only.

## Decision summary

- Support for T06: yes, as a no-go / advisory-only decision gate.
- Support for promotion: no.
- Recommended state: `keep_advisory_only_no_go_for_treatment_v2_promotion`.
