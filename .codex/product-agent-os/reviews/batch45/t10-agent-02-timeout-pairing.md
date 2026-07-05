# B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET sidecar tester/eval-design review

Source status: source-only tester/eval-design review. No provider/live/model/API call, runtime/browser run, target command, git action, CI/blocker change, hook activation, automation or external write was performed.

Review date: 2026-07-05
Role: sidecar tester / eval-design reviewer
Mode: deterministic acceptance design for a future approved rerun
Output artifact: `.codex/product-agent-os/reviews/batch45/t10-agent-02-timeout-pairing.md`

## Scope

Task under review: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`.

This review defines deterministic acceptance criteria for a future approval packet and rerun harness. It does not approve or execute the rerun.

Focus areas:

- run matrix;
- baseline/treatment pairing;
- timeout, no-op and null-score handling;
- retries;
- reviewer route;
- promotion threshold;
- required JSON fields;
- tests that assert source-only and approval boundaries.

Claim ceiling: `source_review_ready_for_t10_packet`; no behavior improvement, treatment v3 success, runtime/browser readiness or promotion is proven.

## Sources Read

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
- `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`
- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`
- `docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json`
- `tests/product_agent_os/test_coding_standards_artifacts.py`
- `TEST.md`
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
- `.codex/product-agent-os/reviews/batch45/t11-agent-02-eval-design.md`
- `.codex/product-agent-os/reviews/batch45/t06-agent-02-test-eval-contract.md`

Memory note: `MEMORY.md` was used only as orientation to locate current Batch 45 source packets. Current repository files above are the evidence source.

## Current Evidence Baseline

`B45-PCA-M26` remains the decisive prior live eval gate:

| Field | Current evidence |
| --- | --- |
| Status | `executed_live_eval_no_go` |
| Baseline average | `4.22` |
| Treatment average | `3.88` |
| Average delta | `-0.34` |
| Completed runs | `15/16` |
| Timeout runs | `1` |
| Advisory warning delta | `29 -> 15` |
| Reviewer decision | `no_go` |
| Decision | `no_go_real_behavior_improvement_not_proven_after_live_eval` |

`B45-POSTQ4-T05` cannot supersede M26:

| Field | Current evidence |
| --- | --- |
| Status | `stopped_on_timeout_inconclusive_no_go` |
| Planned primary task runs | `16` |
| Approved primary task calls started | `2` |
| Completed primary task runs | `1` |
| Timeout primary task runs | `1` |
| Not run due stop rule | `14` |
| Treatment attempted | `0` |
| Reviewer calls started | `0` |
| Delta assessment | `not_comparable_due_early_timeout` |

`B45-POSTQ4-T05B` is necessary but not sufficient: it correctly requires a new exact approval and recommends paired ordering, but T10 should convert that into a stricter result schema and negative-test contract before any future run.

`B45-POSTQ4-T11` is source-only treatment v3 design. It recommends T10 before any approved rerun and explicitly says timeout, no-op and null-score pairs must be quarantined.

## Verdict

T10 should be implemented as a new source-owned approval/harness packet before any new T05B-style run. The future packet should make `paired_continue_after_timeout` the recommended behavior-proof route and treat `strict_stop_on_first_timeout`, `retry_on_timeout` and `single_task_diagnostic` as separate, non-equivalent modes.

The current T05 failure mode was not just "one timeout." The harness design allowed one early baseline timeout to erase all treatment and reviewer evidence. T10 should make that failure impossible to misread by enforcing pair validity, invalid-pair quarantine and reviewer gating in JSON.

## Recommended Run Matrix

The T10 packet should define these modes explicitly:

| Mode | Purpose | Provider/model calls allowed by T10 itself | Promotion evidence? | Pass condition |
| --- | --- | ---: | --- | --- |
| `source_only_preflight` | Validate packet, hashes, matrix, schema and no-action boundaries | `0` | No | JSON packet and tests pass locally. |
| `strict_stop_on_first_timeout` | Cost-safety route | Only after exact future approval | No, unless no timeout occurs | Any timeout records `inconclusive_no_go` and stops. |
| `paired_continue_after_timeout` | Recommended behavior-proof route | Only after exact future approval | Possible | Invalid pairs are quarantined; enough valid pairs remain to satisfy threshold. |
| `retry_on_timeout` | Controlled flake diagnostic | Only after exact future approval and explicit retry budget | Diagnostic by default | Original timeout remains recorded; retry cannot silently replace it. |
| `single_task_diagnostic` | Root-cause a known timeout, for example `B45-HELDOUT-02` | Only after exact diagnostic approval | No | Produces timeout/root-cause evidence only. |
| `reviewer_only_replay` | Score already-completed sanitized summaries | Only after exact reviewer approval if model-backed | No new primary evidence | Reviewer sees completed valid-pair summary and invalid-pair ledger. |

Recommended default for future behavior proof: `paired_continue_after_timeout` with `baseline_then_treatment` inside each task pair, fixed task order, no setup/smoke model calls unless separately approved, and reviewer run only after the valid-pair gate passes.

## Baseline/Treatment Pairing Contract

Each future run should be represented as a task pair, not as two aggregate arms collected in separate phases.

Required pair identity fields:

- `pair_id`: stable value, for example `B45-HELDOUT-02`.
- `task_id`: original held-out task id.
- `task_source_hash`: frozen task text/source hash.
- `baseline_prompt_hash`.
- `treatment_prompt_hash`.
- `treatment_contract_hash`, including the T11 treatment v3 source design when used.
- `model`, `provider_surface`, `sandbox`, `timeout_seconds`, `disposable_root`.
- `arm_order`: recommended `baseline_then_treatment`.

Required valid-pair rule:

- baseline and treatment both have `status == "completed"`;
- both parse final JSON if JSON is required by the harness;
- neither arm has `timed_out == true`;
- neither arm is `no_op`;
- neither arm has `implemented == false` when implementation was required;
- both arms have non-null behavior scores for required dimensions;
- both arms have sanitized changed-file metadata or an accepted no-change reason;
- both arms remain inside the same source freeze.

If any rule fails, the pair status must become one of:

- `invalid_timeout_pair`;
- `invalid_no_op_pair`;
- `invalid_null_score_pair`;
- `invalid_parse_pair`;
- `invalid_unapproved_surface_pair`;
- `invalid_source_drift_pair`;
- `invalid_retention_violation_pair`.

Invalid pairs must not enter average behavior-quality calculations.

## Timeout / No-Op / Null-Score Handling

T10 should hard-code these acceptance rules:

- A timeout is never scored as behavior success.
- A no-op is never scored as behavior success when the task required an edit.
- A null score is never coerced to `0`, `1`, baseline carry-forward, or silently omitted.
- Invalid-pair counts must be displayed with denominators, for example `valid_pairs: 7`, `invalid_pairs: 1`, `planned_pairs: 8`.
- Promotion math must use only valid completed pairs and must also enforce minimum sample size.
- Static advisory warning reduction is reported in a separate namespace and cannot affect pair validity or promotion state.

Recommended minimum sample rule:

- `8/8` valid pairs: eligible for promotion review if all thresholds pass.
- `7/8` valid pairs: `needs_reviewer_or_one_pair_rerun`; not enough for autonomous promotion.
- `<=6/8` valid pairs: diagnostic only; cannot promote.

## Retry Policy

Retries should be forbidden by default. If a future approval explicitly allows retries, T10 should require:

- `max_retries_per_arm`: recommended `1`.
- `retry_reason`: only `timeout`, `wrapper_failure_before_model_call` or `transient_process_failure`.
- `retry_allowed_after_model_output_started`: recommended `false` unless owner accepts possible duplicate-cost ambiguity.
- `original_attempt_retained`: required.
- `retry_attempt_retained`: required.
- `pair_validity_after_retry`: `valid_after_retry` only if the packet states that retry evidence may count; otherwise `diagnostic_after_retry`.
- `promotion_retry_ceiling`: any pair with timeout-plus-retry should require reviewer escalation and cannot be treated as a clean zero-timeout pair.

No silent retries. A retry must never erase `timeout_count`, original exit code, elapsed time, process-kill evidence or cost/call ledger.

## Reviewer Route

The reviewer should run after primary runs only when:

- selected mode is not `single_task_diagnostic`;
- valid-pair count is at least `7`;
- no privacy or raw-retention violation exists;
- no unapproved provider/runtime/browser/target/git/CI/automation surface appears in the packet;
- sanitized per-pair summaries are present.

Reviewer input must include:

- valid-pair score table;
- invalid-pair ledger;
- timeout/no-op/null-score ledger;
- static warning counts separated from behavior scores;
- unsupported claims list;
- source freeze hashes;
- cost/call ledger;
- exact approval id and selected run mode.

Reviewer output must include:

- `reviewer_decision`: `go`, `no_go`, `inconclusive`, or `needs_targeted_rerun`;
- per-dimension deltas;
- critical regressions;
- treatment-specific flake/cost concerns;
- whether static-warning reduction is being over-weighted;
- promotion recommendation with residual risks.

## Promotion Threshold

Promotion should require all of these:

- `promotion_allowed == true` only when future live evidence exists and T10 source-only packet has been superseded by an approved result packet.
- `minimum_behavior_quality_improvement_percent >= 20` over baseline on valid completed pairs.
- `pairwise_quality`: treatment equal-or-better on at least `6/8` planned pairs and no more than one invalid pair.
- `valid_pair_count >= 7`; `8` is required for non-conditional promotion.
- `timeout_count_promotion_counted == 0`.
- `no_op_count_promotion_counted == 0`.
- `null_score_count_promotion_counted == 0`.
- `critical_regression_count == 0`.
- `reviewer_decision` is not `no_go`.
- `static_warning_delta_can_promote == false`.
- `m26_reversed == true` only in a future approved result packet, never in the T10 source-only packet.
- `m35_reversed == true` only if the future result packet explicitly carries enough live behavior evidence and reviewer support.

Any of these should force no-go:

- static-only evidence as promotion basis;
- no treatment arm;
- no reviewer when reviewer is required;
- raw outputs retained in repo;
- target/runtime/browser/provider/git/CI/automation action outside exact approval;
- source drift after freeze;
- invalid pairs hidden from denominators.

## Required T10 JSON Fields

Recommended packet path for the future implementation: `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json`.

Required top-level fields:

- `schema_version`: `batch45_postq4_t10_live_eval_harness_redesign_packet_v1`
- `task_id`: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- `evidence_id`: `B45-POSTQ4-T10-A01`
- `status`: `implemented_source_only_harness_redesign_not_run`
- `source_status`: states no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action was performed.
- `basis`: links M26, T05, T05B, T08, T11 and post-Q4 next tasks.
- `claim_ceiling`: `source_only_harness_redesign_no_behavior_proof`
- `run_modes`: entries for all modes in the run matrix.
- `recommended_mode`: `paired_continue_after_timeout`
- `pairing_contract`
- `valid_pair_rules`
- `invalid_pair_statuses`
- `retry_policy`
- `reviewer_route`
- `promotion_threshold`
- `result_schema_requirements`
- `privacy_retention_policy`
- `cost_call_cap_policy`
- `watchdog_contract`
- `source_freeze_requirements`
- `abort_conditions`
- `unsupported_claims`
- `no_unapproved_actions`
- `control_plane_sync_decision`
- `verification`

Required future result schema fields:

- `approved_run_id`
- `approval_packet_path`
- `approval_scope_digest`
- `provider_surface`
- `model`
- `selected_run_mode`
- `planned_pairs`
- `valid_pairs`
- `invalid_pairs`
- `pair_results[]`
- `aggregate_behavior_scores`
- `aggregate_static_warning_counts`
- `timeout_ledger`
- `no_op_ledger`
- `null_score_ledger`
- `retry_ledger`
- `reviewer_packet`
- `promotion_decision`
- `no_unapproved_actions`
- `raw_retention`
- `unsupported_claims`
- `comparison_to_m26`
- `comparison_to_m35`

## Tests To Add For T10

Add a constant to `tests/product_agent_os/test_coding_standards_artifacts.py` when the T10 packet exists:

```python
POST_Q4_T10_HARNESS = DOCS / "superpowers" / "specs" / "batch45-postq4-t10-live-eval-harness-redesign-packet.json"
```

Add a focused test similar to:

```python
def test_b45_postq4_t10_live_eval_harness_redesign_is_source_only_and_pair_safe(self):
    packet = json.loads(POST_Q4_T10_HARNESS.read_text(encoding="utf-8"))
    next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
    t05 = json.loads(POST_Q4_T05_RESULTS.read_text(encoding="utf-8"))
    t05b = json.loads(POST_Q4_T05B_APPROVAL.read_text(encoding="utf-8"))
    t11 = json.loads(POST_Q4_T11_DESIGN.read_text(encoding="utf-8"))
```

Identity assertions:

- `schema_version == "batch45_postq4_t10_live_eval_harness_redesign_packet_v1"`
- `task_id == "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET"`
- `evidence_id == "B45-POSTQ4-T10-A01"`
- `status == "implemented_source_only_harness_redesign_not_run"`
- `claim_ceiling == "source_only_harness_redesign_no_behavior_proof"`

Run-mode assertions:

- `source_only_preflight`, `strict_stop_on_first_timeout`, `paired_continue_after_timeout`, `retry_on_timeout`, `single_task_diagnostic` are present.
- `recommended_mode == "paired_continue_after_timeout"`.
- `run_modes["source_only_preflight"]["provider_model_calls_allowed"] == 0`.
- `run_modes["single_task_diagnostic"]["promotion_evidence"] is False`.
- `run_modes["strict_stop_on_first_timeout"]["timeout_effect"] == "inconclusive_no_go"`.

Pair-validity assertions:

- `invalid_timeout_pair`, `invalid_no_op_pair` and `invalid_null_score_pair` are in `invalid_pair_statuses`.
- `valid_pair_rules["score_invalid_pairs"] is False`.
- `valid_pair_rules["coerce_null_score"] is False`.
- `valid_pair_rules["static_warning_delta_can_affect_pair_validity"] is False`.
- `minimum_valid_pairs_for_promotion >= 7`.

Timeout/retry assertions:

- retry policy forbids silent retries.
- original timed-out attempt must remain in `retry_ledger`.
- `timeout_count_promotion_counted == 0`.
- `timeout` cannot be counted as behavior success.

Reviewer assertions:

- reviewer route starts only after valid-pair gate.
- reviewer input includes invalid-pair ledger and static warning counts separately.
- reviewer decision must not be `no_go` for promotion.

Boundary assertions:

- every value in `no_unapproved_actions` is `false`;
- `live_model_or_provider_api_called` is `false`;
- `runtime_or_live_server_launched` is `false`;
- `browser_automation_run` is `false`;
- `target_workspace_command_run` is `false`;
- `target_workspace_mutated` is `false`;
- `ci_or_blocker_enforcement_created` is `false`;
- `git_branch_stage_commit_push_pr` is `false`;
- raw outputs in repo are forbidden.

Cross-source assertions:

- T10 basis includes `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T11-A01` and `B45-PCA-M26`.
- T10 references T05 `stopped_on_timeout_inconclusive_no_go`.
- T10 references T11 source-only design but does not claim T11 behavior proof.
- `next_tasks["execution_update"]` points to the T10 packet only after implementation.

Negative fixture tests should also construct an in-memory fake result and assert that:

- a timeout pair cannot enter `aggregate_behavior_scores`;
- a no-op treatment cannot enter promotion math;
- a null-score treatment cannot be coerced into a numeric score;
- static warning delta cannot flip `promotion_allowed`;
- a reviewer `no_go` blocks promotion even when average behavior score improves.

## Recommended Verification Gates For T10

For T10 packet implementation:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

If only this sidecar review file is changed, the smallest meaningful verification is:

```powershell
git diff --check -- .codex/product-agent-os/reviews/batch45/t10-agent-02-timeout-pairing.md
```

Do not run provider/live/model/API, runtime/browser, target, CI/blocker, git mutation, release/deploy/publish or automation checks for T10 without exact owner approval.

## Concrete Recommendations

1. Implement T10 as a source-only JSON packet before any new approval request.
2. Make `paired_continue_after_timeout` the recommended behavior-proof route; keep strict stop and diagnostic modes available but non-promotional unless they complete with no invalid pairs.
3. Require pair-level result validity before aggregates are computed.
4. Treat timeout, no-op and null-score as invalid-pair classes, not weak scores.
5. Require `valid_pair_count >= 7`, reviewer escalation for `7/8`, and diagnostic-only for `<=6/8`.
6. Keep retry disabled by default; if approved, retain original timeout and mark the pair reviewer-required.
7. Keep static warning counts in a separate namespace and assert `static_warning_delta_can_promote == false`.
8. Require reviewer input to include invalid-pair ledger, cost/call ledger, source freeze and unsupported claims.
9. Add negative tests before any approved rerun so invalid pairs cannot silently pass promotion math.
10. Keep T10 source-only until a later exact approval names provider/model, call cap, cost cap, timeout policy, temp root, retention, process kill and reviewer route.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this report does not change accepted project scope.
- `PLAN.md`: `handoff_required`; future T10 implementation should add only a compact pointer if it becomes canonical queue state.
- `TEST.md`: `handoff_required`; promote the T10 verification gates only when the T10 packet exists.
- `EVALS.md`: `handoff_required`; promote pair-validity and invalid-pair threshold policy only if adopted as canonical eval policy.
- `RUNLOG.md`: `not_applicable_for_this_write_scope`; detailed evidence belongs in this source-owned review, not root RUNLOG.
- `prod_test.md`: `not_applicable`; Batch 39 ledger is out of scope.
- `.codex/product-agent-os/lifecycle-state.json`: `accepted_gap_not_written`; user constrained this task to exactly one report file.

RUNLOG overflow decision: `not_applicable`; no RUNLOG edit was made.

## Handoff

- Result: T10 tester/eval-design acceptance review drafted.
- Files changed: `.codex/product-agent-os/reviews/batch45/t10-agent-02-timeout-pairing.md` only.
- Subagents: none.
- Current evidence: source inspection of M26, T05, T05B, T11, T08, post-Q4 queue, tests and control-plane pointers.
- Missing coverage: no T10 JSON packet exists yet; no dedicated T10 tests exist yet; no future live rerun is approved or run.
- Accepted gaps: no lifecycle marker write due exact one-file constraint; no live/provider/runtime/browser/target/git/CI/automation actions by task boundary.
- Retest recommendation: after T10 packet implementation, run `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v` first, then docs/control-plane checks if registry/control-plane files change.
- Recommended next role: builder/docs-maintainer to create the T10 source packet and focused tests; verification agent to run the gates; release/promotion remains no-go until a future approved paired result packet passes thresholds.

## Completion Brief

- Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- Result status: `source_review_ready_for_t10_packet`
- What was done: drafted a sidecar tester/eval-design review for deterministic future rerun acceptance, focused on pairing, timeout/no-op/null-score quarantine, retries, reviewer route, thresholds, JSON fields and source-only tests.
- Files / artifacts changed: `.codex/product-agent-os/reviews/batch45/t10-agent-02-timeout-pairing.md`
- Verification evidence: source files listed above were read; final verification should confirm one-file diff and whitespace hygiene.
- Residual risks / accepted gaps: no T10 packet or tests implemented yet; no live/model/provider rerun approved or run; lifecycle marker not written due exact one-file constraint.
- Follow-up: implement the T10 source JSON packet and focused assertions before any future T05B-style approval or rerun.
