# B45 T10 Live-Eval Harness Redesign - Architecture Review

Source status: source-only sidecar architecture review. No live/model/provider/API call, runtime/browser action, target command, git action, CI/automation, release, deployment or external write was performed.

## Scope

Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`

Purpose: recommend the smallest viable architecture boundary for a future Batch 45 live-eval harness redesign packet after M26 no-go and T05 timeout.

Owned output: `.codex/product-agent-os/reviews/batch45/t10-agent-01-eval-architecture.md`

Forbidden surfaces for this sidecar review:

- live/model/provider/API calls;
- runtime servers, browser automation, target workspace commands or target mutation;
- git branch/stage/commit/push/PR;
- CI/blocker/automation creation or activation;
- edits to root control-plane files, source specs, lifecycle marker or registry files.

Subagents: none used.

## Sources Read

| Source | Claim used | Freshness | Confidence | Conflict / limit |
| --- | --- | --- | --- | --- |
| `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` | M26 live eval remains no-go: treatment reduced advisory warnings but scored lower than baseline, had one timeout, and reviewer decision was `no_go`. | 2026-06-30 packet | high | Prior live run, not post-Q4 treatment v3 proof. |
| `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json` | T05 consumed approved live/model scope but stopped after baseline timeout; treatment and reviewer did not run, so result is inconclusive/no-go. | 2026-07-04 packet | high | Raw traces temp-only; repo has sanitized rollup only. |
| `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json` | Future rerun needs new exact approval, paired ordering is recommended, strict stop / paired continue / diagnostic modes are named, and watchdog/retention boundaries are required. | 2026-07-04 packet | high | Approval packet only; no rerun executed. |
| `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json` | T10 is recommended before any new T05B run; future packet must separate timeout policies, reviewer timing, cost, retention and abort conditions. | 2026-07-04 packet | high | Source-owned architecture route, not implementation. |
| `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json` | Treatment v3 is source-only and requires T10 before future rerun; invalid timeout/no-op/null-score pairs must be quarantined. | 2026-07-05 packet | high | Does not prove behavior improvement. |
| `docs/superpowers/specs/batch45-post-q4-next-tasks.json` | T10 status is recommended before any new run; acceptance includes strict stop, paired continue, retry-on-timeout, diagnostic-only routes and no provider calls during packet prep. | 2026-07-04 packet with T11 update | high | Planning source, not execution evidence. |
| `.codex/workflows/coding-standards.md` | Future code-bearing harness changes need existing-capability scan, no new dependency by default, small seams and evidence before code-quality claims. | current workflow | high | Not applicable to this report as implementation; applicable to future harness code. |
| `.codex/artifact-templates/coding-standard-checklist.md` | Checklist fields for future implementation handoff: leverage path, dependency decision, module/legacy safety, evidence, unsupported claims. | current template | high | This sidecar records reduced evidence only. |

## Current Architecture Problem

The live-eval harness currently has an evidence fragility problem, not just a timeout problem.

M26 produced a complete-enough baseline/treatment comparison and ended `no_go`: baseline average was `4.22`, treatment average was `3.88`, treatment was worse on 4 of 8 tasks, one treatment run timed out, and independent reviewer decision was `no_go`.

T05 then tried a post-Q4 live/model rerun, but the baseline-first schedule plus `stop_on_timeout` meant one baseline timeout on `B45-HELDOUT-02` prevented all treatment and reviewer evidence. That result cannot supersede M26 and increases confidence that flake/cost control remains a blocker.

Therefore T10 should redesign the harness around comparable task pairs, explicit invalid-pair quarantine and a promotion decision that cannot be inferred from static warning deltas or incomplete arms.

## Recommendation

Selected option: `paired_continue_after_timeout_with_invalid_pair_quarantine` as the default architecture for the next approval packet.

Rationale:

- It preserves per-task comparability by running baseline and treatment as a pair before moving to the next task.
- It prevents one timeout from erasing the full treatment arm, which happened in T05.
- It still protects promotion quality by quarantining incomplete, timed-out, no-op or null-score pairs from behavior-improvement calculations.
- It keeps cost bounded through an explicit max-pairs, max-timeout and owner-approved call-count cap.

Rejected as default:

- `baseline_first_legacy`: reproduces T05 comparability risk.
- `strict_stop_on_first_timeout`: useful for cost-safety no-go behavior, but too brittle for learning whether treatment v3 improves comparable tasks.
- `single_task_diagnostic`: valid for timeout forensics only; cannot support promotion.
- `retry_on_timeout_as_success_path`: unsafe for promotion unless the retry policy is separately approved and retry outcomes remain marked as diagnostic or quarantined.

## Pairing Model

Primary unit of evidence: `task_pair`.

Recommended run order per held-out task:

1. prepare disposable copy for the task pair;
2. run `baseline`;
3. run `treatment`;
4. collect sanitized per-run metadata;
5. classify pair as `valid_comparable`, `invalid_timeout`, `invalid_noop`, `invalid_write_boundary`, `invalid_parse`, `invalid_score_gap` or `diagnostic_only`;
6. continue to the next pair only if the selected timeout/cost policy permits it.

Promotion-counted pairs must meet all conditions:

- baseline and treatment both completed;
- final JSON or final status parsed;
- behavior scores exist for both arms;
- no timeout in either arm;
- no no-op caused by writeability/sandbox boundary;
- no raw private output persisted in repo;
- no unapproved action occurred;
- reviewer has enough sanitized evidence to compare the pair.

Pair-level quarantine is mandatory. A quarantined pair may inform flake/root-cause analysis, but it must not improve averages, pairwise win counts or promotion thresholds.

## Timeout Policy Options

### Option A: `strict_stop_on_first_timeout`

Use when owner prioritizes cost safety over evidence completeness.

Rules:

- any timeout stops all remaining primary runs;
- reviewer does not run unless a comparable score table already exists;
- decision becomes `inconclusive_no_go`;
- promotion is forbidden.

### Option B: `paired_continue_after_timeout_with_quarantine`

Recommended default for behavior proof.

Rules:

- timeout quarantines the current `task_pair`;
- process tree kill and lingering-process check are required;
- remaining pairs may continue until approved call/time/cost caps are reached;
- promotion requires enough valid comparable pairs and zero promotion-counted timeouts.

Minimum valid sample recommendation:

- target: 8 valid comparable pairs;
- hard floor: 6 valid comparable pairs only if owner explicitly accepts reduced sample size before the run;
- below floor: `inconclusive_no_go`.

### Option C: `single_task_diagnostic`

Use only to diagnose known timeout risk such as `B45-HELDOUT-02`.

Rules:

- may target one task or one pair;
- cannot support treatment promotion;
- result status must be `diagnostic_only`;
- reviewer is optional and should focus on timeout root cause, not promotion.

### Option D: `bounded_retry_on_timeout`

Use only with exact owner approval.

Rules:

- one retry maximum per timed-out arm or pair;
- retry call count must be included in approval cap;
- original timeout remains recorded;
- retried pair defaults to `diagnostic_only` or `invalid_timeout_retry`;
- promotion counting requires an explicit owner-approved rule before the run, otherwise retries cannot contribute to promotion.

Forbidden timeout behavior:

- silent retries;
- treating timeout partial patches as completed implementation;
- averaging null scores into behavior quality;
- running reviewer after timeout when no comparable score table exists;
- retaining raw timeout output in repo.

## Invalid-Pair Quarantine

Quarantine classifications should be explicit and mutually exclusive where possible:

- `invalid_timeout`: baseline or treatment exceeded approved timeout.
- `invalid_noop`: no implementation occurred because target file, `.codex`, sandbox or write boundary prevented the intended change.
- `invalid_parse`: final JSON/status could not be parsed.
- `invalid_score_gap`: one or more required rubric dimensions are null without an accepted reason.
- `invalid_unapproved_surface`: run touched a forbidden or unapproved surface.
- `invalid_retention`: raw private prompt/output/trace would need repo retention.
- `diagnostic_only`: owner-approved diagnostic path, not behavior proof.

Quarantine effects:

- excluded from `valid_pair_count`, averages, pairwise win/loss counts and promotion thresholds;
- included in flake/cost/privacy ledger;
- included in reviewer context only as risk evidence;
- cannot reverse M26/M35 no-go.

## Reviewer Timing

Reviewer should run only after primary runs produce a sanitized comparable table that meets the selected policy.

Recommended timing:

1. primary paired runs complete or stop by policy;
2. harness builds sanitized `task_pairs` and `quarantine` tables;
3. harness checks minimum valid-pair floor;
4. if floor is met, run one independent reviewer on sanitized rollup only;
5. if floor is not met, do not run reviewer unless owner approved diagnostic review;
6. promotion decision consumes primary metrics plus reviewer decision.

Reviewer must not:

- fill missing scores;
- convert quarantined pairs into valid evidence;
- inspect raw private traces retained in repo;
- override a `no_go` caused by approval, retention or unapproved-action breach.

## Result Schema

Recommended source-owned result packet schema:

```json
{
  "schema_version": "batch45_live_eval_harness_result_v2",
  "task_id": "B45-POSTQ4-T10-or-future-run-id",
  "evidence_id": "B45-POSTQ4-Txx-A01",
  "status": "completed_paired_eval | inconclusive_no_go | stopped_on_timeout_no_go | diagnostic_only",
  "source_status": "sanitized rollup only; raw outputs temp-only",
  "approval_used": {
    "provider_surface": "...",
    "model": "...",
    "approved_primary_task_pairs": 8,
    "approved_reviewer_calls": 1,
    "approved_retry_calls": 0,
    "timeout_policy": "paired_continue_after_timeout_with_quarantine",
    "timeout_seconds_per_arm": 600,
    "cost_cap": "...",
    "retention": "raw outputs temp-only; repo stores sanitized rollup only"
  },
  "source_freeze": {
    "eval_plan": {"path": "...", "sha256": "..."},
    "approval_packet": {"path": "...", "sha256": "..."},
    "treatment_contract": {"path": "...", "sha256": "..."},
    "scoring_rubric": {"path": "...", "sha256": "..."}
  },
  "execution_summary": {
    "planned_pairs": 8,
    "valid_pair_count": 0,
    "quarantined_pair_count": 0,
    "timeout_count": 0,
    "reviewer_calls_started": 0,
    "stop_reason": "...",
    "decision_impact": "does_not_reverse_M26_or_M35_no_go | ..."
  },
  "task_pairs": [
    {
      "task_id": "B45-HELDOUT-01",
      "pair_status": "valid_comparable",
      "baseline_run_id": "...",
      "treatment_run_id": "...",
      "baseline_score": 0.0,
      "treatment_score": 0.0,
      "delta": 0.0,
      "winner": "baseline | treatment | equal",
      "promotion_counted": true
    }
  ],
  "runs": [
    {
      "run_id": "...",
      "task_id": "...",
      "arm": "baseline | treatment",
      "status": "completed | timeout_partial_patch | no_op | parse_failed",
      "started_at": "...",
      "ended_at": "...",
      "elapsed_seconds": 0.0,
      "timed_out": false,
      "exit_code": 0,
      "final_json_parse_ok": true,
      "changed_file_count": 0,
      "changed_files": [{"path": "...", "change_type": "modified"}],
      "advisory_warning_count": 0,
      "behavior_scores": {},
      "raw_retention": {
        "raw_outputs_location": "temp_only",
        "stdout_sha256": "...",
        "stderr_sha256": "...",
        "prompt_sha256": "..."
      }
    }
  ],
  "quarantine": [
    {
      "task_id": "...",
      "reason": "invalid_timeout",
      "affected_arms": ["baseline"],
      "promotion_counted": false,
      "diagnostic_use_allowed": true
    }
  ],
  "reviewer": {
    "status": "not_run_due_insufficient_valid_pairs | completed",
    "decision": "go | no_go | diagnostic_only | not_applicable",
    "decision_reason": "..."
  },
  "promotion_threshold_result": {
    "static_warning_delta_can_promote": false,
    "minimum_behavior_quality_improvement_met": false,
    "pairwise_quality_met": false,
    "timeout_requirement_met": false,
    "reviewer_requirement_met": false,
    "promotion_allowed": false
  },
  "no_unapproved_actions": {},
  "unsupported_claims": [],
  "verification": {}
}
```

Schema constraints:

- `advisory_warning_count` is reported separately from behavior score.
- `promotion_counted` must be false for every quarantined pair.
- `static_warning_delta_can_promote` must remain false.
- `reviewer` must be separate from primary task output.
- `no_unapproved_actions` must distinguish approved live/model calls from unapproved actions.

## Approval Boundaries

Preparing T10 design may be local/source-only. Running the harness requires a new exact approval packet.

Future run approval must name:

- provider surface and exact model;
- primary pair count and arm count;
- reviewer call count;
- retry call count, if any;
- timeout per arm and outer watchdog policy;
- cost cap or accepted cost gap;
- disposable temp root pattern and cleanup policy;
- raw retention boundary;
- command surface;
- forbidden surfaces;
- stop conditions.

Approval cannot be inherited from T05. T05 approval was consumed.

## Trust, Privacy And Operations Boundary

Trust boundary:

- repo stores sanitized rollups, hashes, aggregate scores and changed-file metadata only;
- temp-only raw outputs may exist during approved run execution;
- target workspaces are not mutated unless a separate approval names the target, rollback and evidence route;
- reviewer consumes sanitized evidence, not raw private traces.

Operational requirements for a future implementation:

- external non-model watchdog around each arm;
- scoped process-tree kill on timeout;
- lingering-process check scoped to disposable root/run id;
- write probe for disposable temp root before any model call;
- no setup/smoke model calls unless explicitly approved;
- final no-unapproved-actions ledger.

## Professional Code Authoring Route For Future Harness Changes

This sidecar review is docs-only and source-only, so the coding-standard checklist is `not_applicable` for implementation evidence.

Future code-bearing T10 implementation should use:

- selected leverage path: `project_helper` or `tiny_adapter` before new custom subsystem;
- dependency posture: no new dependency by default;
- existing capability scan: reuse current Batch 45 packet patterns, sanitized rollup shape, approval ledger, raw-temp-only retention policy, and existing Python/PowerShell process controls where present;
- rejected broad rewrite: do not rewrite the full eval framework or scoring rubric from first principles;
- rollback path: revert only the future T10 packet/harness files touched in that slice and preserve M26/T05/T05B evidence packets.

## Stop Conditions

Stop before any future run if:

- exact owner approval is missing or ambiguous;
- model/provider/surface/cost cap/run count/timeout policy is ambiguous;
- temp root write probe or cleanup safety fails;
- watchdog cannot kill scoped process tree;
- raw prompts, raw outputs, provider payload bodies, private source bodies, secrets or credentials would be retained in repo;
- a task requires target workspace mutation, runtime/browser launch, database access or provider call outside approval;
- result schema would count timeout/no-op/null-score pairs as valid behavior evidence;
- reviewer would be asked to decide promotion without minimum valid comparable pairs;
- wording implies M26/M35 no-go is reversed before a completed comparable live eval exists.

## Control-Plane Sync Decision

Per `.codex/workflows/control-plane-sync.md`, this sidecar changes no root scope, queue, verification command, eval threshold or current-cycle handoff file because the user explicitly allowed exactly one report file.

- `REQUIREMENTS.md`: `not_applicable_no_scope_change`
- `PLAN.md`: `handoff_required_if_owner_wants_T10_queue_sync`
- `TEST.md`: `handoff_required_if_owner_wants_future_harness_checks_recorded`
- `EVALS.md`: `handoff_required_if_owner_wants_threshold_schema_sync`
- `RUNLOG.md`: `handoff_required_due_exact_one_file_scope_and_budget_sensitivity`
- `prod_test.md`: `not_applicable_batch39_surface`
- `.codex/product-agent-os/lifecycle-state.json`: `not_updated_due_exact_one_file_scope`

## Architecture Decision

Decision: T10 should specify a paired live-eval harness with invalid-pair quarantine as the default future run architecture.

Status: recommended for owner review; not implemented; not approved for execution.

Consequences:

- future live/model rerun can learn from remaining valid pairs after a timeout;
- promotion remains blocked unless valid comparable pairs meet behavior thresholds and reviewer is not `no_go`;
- timeout, no-op, null-score and approval-boundary failures become explicit risk evidence instead of contaminating averages;
- the harness remains approval-bound and source-owned until a separate implementation/run task is approved.

## Completion Brief

- Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- Result status: `source_only_architecture_review_written`
- What was done: reviewed the six requested Batch 45 source packets plus coding-standard workflow/checklist constraints and produced a sidecar architecture recommendation for T10 live-eval harness redesign.
- Files / artifacts changed: `.codex/product-agent-os/reviews/batch45/t10-agent-01-eval-architecture.md`
- Verification evidence: source files were read with `Get-Content`; target directory existence was checked with `Get-Item`; report file did not exist before creation according to `Test-Path`; no live/model/provider/API call, runtime/browser, target command, git, CI/automation or external write was performed.
- Assumptions: T10 remains packet/design work until owner gives a separate exact approval for any live/model rerun; source packets are current source truth for this sidecar review.
- Residual risks / accepted gaps: lifecycle marker and root control-plane files were not updated because the user required exactly one report file; no JSON/schema test was added; no future harness implementation was verified.
- Follow-up: next owner route is to convert this recommendation into the T10 approval packet/schema update, then request exact owner approval only if a live/model rerun is desired.
