# Product-Agent OS Track 10 backlog

Source status: `internal`

This backlog tracks deferred and follow-up work for Track 10 `Task 23: Guided Question Protocol And Project Status Dashboard`.

## Batch 5 Closure

| Status | Item | Notes |
| --- | --- | --- |
| `done` | `T10-Q-M15..M22` eval, skills and docs coverage | Added `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, and `stale_evidence_no_success_claim`. |
| `done` | Guided question behavioral/transcript coverage | Added `guided-question-smallest-blocking-question`, `guided-question-no-broad-methodology-interview`, `status-dashboard-generated-view-only`, `status-dashboard-stale-evidence-no-success-claim`, and `runtime-first-response-no-question-dump`. |
| `done` | Lifecycle skill protocol wording | Skills now ask the smallest blocking question only, keep optional questions in the packet, route answers into artifacts or accepted gaps, and do not use guided questions as workspace evidence. |

## Batch 6 Closure

| Status | Item | Notes |
| --- | --- | --- |
| `done` | `T10-Q-M23` focused/full unit verification | Full unit discovery ran 543 tests with `OK` after focused behavioral-template contract fixes. |
| `done` | `T10-Q-M24` full Product-Agent OS verification | Fixture eval exited `0` with `renderer_file_count: 187`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs and `git diff --check` exited `0`. |
| `done` | `T10-Q-M25` explicit-only git boundary | No `git add`, `git commit`, `git push` or PR creation was executed. |

## Deferred

| Status | Item | Reason |
| --- | --- | --- |
| `deferred` | Interactive dashboard editing | `status.html` remains a generated view; editing state in the dashboard would create a second source of truth. |
| `deferred` | Dashboard web server | Current scope is static offline HTML/JSON only; no standalone server or long-running process. |
| `deferred` | Live external telemetry widgets | External assets and external systems remain approval-bound and out of scope for the offline dashboard. |
| `deferred` | LLM semantic judge for question quality | Current transcript eval is deterministic term replay; calibrated judge coverage needs its own eval design and privacy policy. |

## Verification

Batch 5 focused verification and Batch 6 full verification are recorded in `TEST.md` and `RUNLOG.md`.
