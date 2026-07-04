# B45-POSTQ4-T06-PROMOTION-DECISION test/eval contract

Source status: verification/test-contract analysis only. No core files changed. No live/model/provider/runtime/browser/target/git actions were run.

## Scope

- Task: `B45-POSTQ4-T06-PROMOTION-DECISION`.
- Output artifact: `.codex/product-agent-os/reviews/batch45/t06-agent-02-test-eval-contract.md`.
- Primary files read:
  - `tests/product_agent_os/test_coding_standards_artifacts.py`
  - `TEST.md`
  - `EVALS.md`
  - `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
  - `docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json`
  - `docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json`
  - `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
  - `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`
  - `docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json`
  - `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
  - `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`
  - `docs/superpowers/specs/batch45-real-project-scorecard.json`
  - `docs/superpowers/specs/batch45-real-project-decision-packet.json`
  - `.codex/product-agent-os/reviews/batch45/t06-agent-01-source-evidence.md`

## Current Contract Gap

`B45-POSTQ4-T06-PROMOTION-DECISION` is currently present as a planned `decision_gate` in `batch45-post-q4-next-tasks.json`, and T05 recommends it as the next no-go-preserving decision. There is no separate T06 decision packet JSON yet, and `tests/product_agent_os/test_coding_standards_artifacts.py` has no dedicated assertion block for that future packet.

Existing tests already assert:

- T06 exists in the post-Q4 task queue.
- T01-T03 reduced static warnings from `14` to `0`.
- T05 ended as `stopped_on_timeout_inconclusive_no_go`.
- T05B is `approval_packet_only_not_run`.
- Static warning delta cannot promote.
- M26/M35 no-go boundaries remain unreversed.

Missing test contract: a future `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json` packet must be asserted directly.

## Assertions To Add

Add a new constant in `tests/product_agent_os/test_coding_standards_artifacts.py`:

```python
POST_Q4_T06_DECISION = DOCS / "superpowers" / "specs" / "batch45-postq4-t06-promotion-decision.json"
```

Add a focused test, for example:

```python
def test_b45_postq4_t06_promotion_decision_preserves_no_go(self):
    packet = json.loads(POST_Q4_T06_DECISION.read_text(encoding="utf-8"))
    next_tasks = json.loads(POST_Q4_NEXT_TASKS.read_text(encoding="utf-8"))
    t05 = json.loads(POST_Q4_T05_RESULTS.read_text(encoding="utf-8"))
    t05b = json.loads(POST_Q4_T05B_APPROVAL.read_text(encoding="utf-8"))
    m26 = json.loads(M26_RESULTS.read_text(encoding="utf-8"))
    m27 = json.loads(M27_DECISION.read_text(encoding="utf-8"))
    m35 = json.loads(M35_DECISION.read_text(encoding="utf-8"))
```

Required packet identity assertions:

- `schema_version == "batch45_postq4_t06_promotion_decision_v1"`
- `task_id == "B45-POSTQ4-T06-PROMOTION-DECISION"`
- `evidence_id == "B45-POSTQ4-T06-A01"`
- `status` should encode no-go, for example `implemented_promotion_no_go_keep_advisory_only`
- `decision.state == "keep_advisory_only_no_go_for_treatment_v2_promotion"` or an explicitly equivalent no-go state such as `no_go_preserve_advisory_only_static_delta_not_sufficient`
- `decision.keep_advisory_only is True`
- `decision.promotion_allowed is False`
- `decision.ci_or_blocker_promotion_allowed is False`
- `decision.static_warning_delta_can_promote is False`
- `decision.m26_reversed is False`
- `decision.m35_reversed is False`
- `decision.t05_reversed is False`

Required evidence-link assertions:

- `evidence_used` includes these task/evidence IDs and all referenced `source` paths exist:
  - `B45-POST-Q4-NEXT-TASKS-A01`
  - `B45-POSTQ4-T01-T04-A01`
  - `B45-POSTQ4-T05-A01`
  - `B45-POSTQ4-T05B-A01`
  - `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`
  - `B45-PCA-M26`
  - `B45-PCA-M27`
  - `B45-PCA-M34-A01`
  - `B45-PCA-M35-A01`

Required static-delta assertions:

- `static_delta.q4_baseline_warning_count == 14`
- `static_delta.post_t03_warning_count == 0`
- `static_delta.delta == -14`
- `static_delta.unresolved_advisory_warnings == 0`
- `static_delta.blocking is False`
- `static_delta.suppressed_warning_count == 0`
- `static_delta.evidence_class == "local_static_copied_fixture_warning_delta_only"`
- A negative assertion that static delta is not used as behavior proof, e.g. serialized packet contains `static_warning_delta_can_promote` and that value is false.

Required live-eval/no-go assertions:

- `live_eval.t05_status == "stopped_on_timeout_inconclusive_no_go"`
- `live_eval.planned_primary_task_runs == 16`
- `live_eval.approved_primary_task_model_calls_started == 2`
- `live_eval.completed_primary_task_runs == 1`
- `live_eval.timeout_primary_task_runs == 1`
- `live_eval.not_run_due_stop_rule == 14`
- `live_eval.treatment_completed_runs == 0`
- `live_eval.reviewer_calls_started == 0`
- `live_eval.delta_assessment == "not_comparable_due_early_timeout"`
- `live_eval.m26_reversed is False`
- `live_eval.m35_reversed is False`

Required T05B approval-only assertions:

- `t05b_basis.status == "approval_packet_only_not_run"`
- `t05b_basis.new_exact_approval_required is True`
- `t05b_basis.raw_outputs_in_repo_allowed is False`
- `t05b_basis.static_warning_delta_can_promote is False`
- No field in the T06 packet treats T05B as execution evidence.

Required decision-matrix assertions:

- `decision_matrix.keep_advisory_only.decision == "selected"`
- `decision_matrix.promote_ci_or_blocker.decision == "rejected"`
- `decision_matrix.claim_real_ai_agent_behavior_improvement.decision == "rejected"`
- `decision_matrix.request_new_live_model_rerun.decision == "approval_required"` if included.
- `decision_matrix.request_runtime_browser_packet.decision == "approval_required"` if included.
- Any "run more pilots" route is either `deferred`, `approval_required`, or `source_only_future_option`, not promoted.

Required approval/no-action assertions:

- Every value in `no_unapproved_actions` is false.
- If `approved_actions_performed` is included, it must be limited to the already recorded T05 approved Codex CLI/OpenAI calls: started `2`, completed `1`, timed out `1`.
- No field may imply new provider/model/API calls, runtime launch, browser automation, target workspace command/mutation, database access, CI/blocker enforcement, git branch/stage/commit/push/PR, release/deploy/publish, active automation, or external write during T06.

Required unsupported-claims assertions:

The packet must include these unsupported claims, or exact equivalents:

- `real_ai_agent_behavior_improvement`
- `treatment_v2_promotion_readiness`
- `ci_or_blocker_enforcement_readiness`
- `target_runtime_behavior`
- `browser_behavior`
- `provider_or_live_api_behavior`
- `target_workspace_safety_after_mutation`
- `database_or_production_data_safety`
- `release_deploy_publish_readiness`
- `active_automation_readiness`
- `M26_no_go_reversed`
- `M27_promotion_no_go_reversed`
- `M35_no_go_reversed`
- `SOL_TypeScript_runtime_validated`
- `myPartners_CRM_behavior_validated`

Required control-plane/source assertions after a future T06 implementation:

- `docs/sources/registry.md` and `docs/sources/registry.en.md` mention `B45-POSTQ4-T06-A01` and the T06 packet path.
- `PLAN.md`, `TEST.md`, `EVALS.md`, and Track 11 plan include compact pointers for T06.
- `RUNLOG.md` should be `handoff_required_due_runlog_budget` or a compact current-state pointer only, not a detailed ledger.
- Lifecycle marker may point to T06 only if the implementation slice is allowed to update `.codex/product-agent-os/lifecycle-state.json`.

## Verification Gates For T06

Minimum local gates for the future T06 decision packet:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Add this focused gate when T06 touches or depends on local advisory/lifecycle hook boundaries:

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
```

Do not require strict MkDocs unless T06 changes MkDocs nav, Mermaid, localized docs navigation, search/sitemap, generated `site/`, or a public documentation page that must be rendered.

Do not run live/model/provider/runtime/browser/target/git mutation gates for T06 unless the owner gives a separate exact approval packet. T06 can recommend such gates as follow-up, but the decision packet itself must not execute them.

## Claims That Must Remain Unsupported

T06 may claim:

- local/static copied-fixture warning delta is `14 -> 0`;
- T05 was an approved live/model attempt but stopped on timeout;
- T05 did not produce comparable baseline-vs-treatment evidence;
- T05B is approval-packet-only and needs new exact approval;
- existing M26/M27/M35 no-go/advisory-only boundaries remain active;
- advisory-only/no-go is the supported decision.

T06 must not claim:

- real AI-agent behavior improvement;
- treatment v2 promotion readiness;
- CI or blocker promotion readiness;
- active automation readiness;
- runtime/browser/provider/API behavior proof;
- target workspace mutation safety;
- database or production-data safety;
- release/deploy/publish readiness;
- SOL TypeScript runtime validation;
- myPartners CRM behavior validation;
- M26/M27/M35 reversal;
- that static warning reduction is enough for promotion;
- that T05B approval-packet design is execution evidence.

## Retest Recommendation

Smallest retest after adding the T06 packet and assertions:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
```

If that passes and T06 also updates source registry/control-plane pointers, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

If `git diff --check` is disallowed in a given approval boundary, record it as an accepted gap rather than replacing it with generated-view evidence.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this analysis does not change scope or acceptance.
- `PLAN.md`: `handoff_required` for future T06 implementation only; not updated in this report-only slice.
- `TEST.md`: `handoff_required` for future T06 gate routing only; not updated in this report-only slice.
- `EVALS.md`: `handoff_required` for future T06 claim ceiling only; not updated in this report-only slice.
- `RUNLOG.md`: `handoff_required_due_runlog_budget`; no update in this report-only slice.
- `prod_test.md`: `not_applicable`.
- Source registry: `handoff_required` after future T06 packet exists; not updated in this report-only slice.

## Handoff

- Result: test/eval contract drafted for T06.
- Current evidence: source inspection only; no current unit/docs gates were run.
- Missing coverage: dedicated T06 decision packet and dedicated `test_coding_standards_artifacts.py` assertions.
- Recommended next role: builder or docs-maintainer to create the T06 packet and add focused assertions; verification agent to run the gates above.
- Stop condition preserved: no live/model/provider/runtime/browser/target/git actions without exact approval.
