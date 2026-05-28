# Product-Agent OS Track 10 backlog

Source status: `internal`

This backlog tracks deferred and follow-up work for Track 10 `Task 23: Guided Question Protocol And Project Status Dashboard` and `Task 24: Self-Verification And Modernization Loop`.

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

## Task 24 Batch 7 Closure

| Status | Item | Notes |
| --- | --- | --- |
| `done` | `T10-SV-M-1..M4` foundation and registry | Added `agent_skill_metrics.py` with read-only source-priority policy, target registry collection, explicit evidence intake and bounded metrics packet helpers. |
| `done` | `T10-SV-G1..G3` reuse/source/bounds guardrails | Reused runtime redaction, rejected dashboard/report HTML, memory, raw chat logs and unsupported community claims as source of truth, and trimmed oversized metrics packets deterministically with warnings. |
| `done` | Batch 7 focused and full verification evidence | `test_agent_skill_metrics` failed before implementation on missing module and stale evidence support, then ran 5 tests with `OK`; adjacent status/dashboard/template/automation checks ran 103 tests with `OK`; full unittest ran 548 tests with `OK`; fixture eval, transcript eval, Codex compatibility, docs check and `git diff --check` exited `0`. |
| `done` | Task 24 Batch 8 `T10-SV-M5..M16` | Added trace normalization, metrics redaction gate blocking, evidence dataset builder, dataset quality gates, local grader summary and judge calibration summary in `agent_skill_metrics.py`. |
| `done` | Batch 8 focused and full verification evidence | Batch 8 RED failed on missing imports, then focused tests ran 11 tests with `OK`; adjacent status/dashboard, template/automation and slow fixture/transcript runner checks ran 22, 87 and 21 tests with `OK`; full unittest ran 554 tests with `OK`; fixture eval, transcript eval, Codex compatibility, docs check and `git diff --check` exited `0`. |
| `queued` | Task 24 Batch 9 | Metrics, scorecards, confidence and cadence remain next. |

## Deferred

| Status | Item | Reason |
| --- | --- | --- |
| `deferred` | Interactive dashboard editing | `status.html` remains a generated view; editing state in the dashboard would create a second source of truth. |
| `deferred` | Dashboard web server | Current scope is static offline HTML/JSON only; no standalone server or long-running process. |
| `deferred` | Live external telemetry widgets | External assets and external systems remain approval-bound and out of scope for the offline dashboard. |
| `deferred` | LLM semantic judge for question quality | Current transcript eval is deterministic term replay; calibrated judge coverage needs its own eval design and privacy policy. |

## Verification

Batch 5 focused verification and Batch 6 full verification are recorded in `TEST.md` and `RUNLOG.md`.
