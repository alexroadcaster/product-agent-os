# Product-Agent OS Track 10 backlog

Source status: `internal`

This backlog tracks deferred and follow-up work for Track 10 `Task 23: Guided Question Protocol And Project Status Dashboard`, `Task 24: Self-Verification And Modernization Loop` and `Task 25: Project Code Graph And HTML Cockpit Visualization`.

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
| `done` | Task 24 Batch 9 `T10-SV-M17..M28` | Added metric aggregation, repeatability metrics, guarded scorecards, confidence/decision gates, cadence recommendation and deterministic redacted run records in `agent_skill_metrics.py`. |
| `done` | Batch 9 focused and full verification evidence | Batch 9 RED failed on missing imports, then focused tests ran 17 tests with `OK`; adjacent status/dashboard, template/automation and slow fixture/transcript runner checks ran 28, 87 and 21 tests with `OK`; full unittest ran 560 tests with `OK` in 809.106s using `timeout_ms: 900000`; fixture eval, transcript eval, Codex compatibility, docs check and `git diff --check` exited `0`. |
| `done` | Task 24 Batch 10 `T10-SV-M29..M45` plus `T10-SV-G4..G6` | Added trace data-classification, shared offline artifact safety, scorecard ledger, daily/weekly metrics packets, component prioritization, modernization candidates, redacted offline report renderer, dry-run/stage CLI and metrics automation candidate-only blocking. |
| `done` | Batch 10 focused and full verification evidence | Batch 10 RED failed on missing imports/modules/templates and metrics automation blocking, then focused tests ran 127 tests with `OK`; fixture runner unit suite ran 17 tests with `OK`; full unittest ran 575 tests with `OK` in 612.098s using `timeout_ms: 1200000`; fixture eval exited `0` with 80 fixtures and `renderer_file_count: 191`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check and `git diff --check` exited `0`. |
| `done` | Task 24 Batch 11 `T10-SV-M46..M57` | Added bounded status snapshot summaries, discovery/applicability and methodology audit routing, runtime packet validation, review-only finish options, guided question integration, lifecycle skill wording, fixture false-positive coverage, behavioral eval cases, transcript sessions and batch status sync. |
| `done` | Batch 11 focused and broad verification evidence | Batch 11 RED failed on missing status/discovery/audit/runtime/lifecycle/eval contracts, then focused tests ran 306 tests with `OK`; full unittest ran 583 tests with `OK` in 636.067s using `timeout_ms: 1200000`; fixture eval exited `0` with 85 fixtures, 0 failures and `renderer_file_count: 191`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs/source-policy slice ran 22 tests with `OK`; docs check and `git diff --check` exited `0`. |
| `done` | `T10-SV-M58..M62` final docs/control-plane verification closure | Task 24 Batch 12 synchronized Product-Agent OS docs, root/plugin READMEs, source registry, Track 10 backlog and root control-plane evidence for `agent_skill_metrics_loop`; full unittest must use `timeout_ms: 1200000`; commit/push/PR remains an explicit-only git boundary. |

## Task 25 Batch 13-16 Closure

| Status | Item | Notes |
| --- | --- | --- |
| `done` | `T10-CG-V2-M01..M07` graph foundation | Added read-only, stage-first graph JSON/JSONL foundation with controlled ontology/schema validation, manifest freshness/provenance, observation lineage, temporal edge helpers, stage-local safety and scale fixtures. |
| `done` | `T10-CG-V2-M08..M13` scanner overlays | Added Python AST package/module/class/function/method overlays, conservative import/call/test edges, unsupported-language adapter boundaries, structured docs/contracts/schema/diagram overlays, partition scopes, canonical aliases and bounded readiness metadata. |
| `done` | `T10-CG-V2-M14..M18` graph query/runtime/analysis | Added graph-only query packets, query CLI mode, budget/filter safety, trace/impact/affected-test/delta/read-order packets, runtime/status graph summaries, lifecycle source-of-truth wording and source-free analysis reports. |
| `done` | `T10-CG-V2-M19..M26` cockpit visualization | Added eight-page cockpit model, offline stage-only HTML/JSON renderer, Code Flow inside `Code Intelligence`, Graphology-compatible static visual projection, local Graphology/Sigma vendor boundary, filters, focused subgraphs, selected-node evidence, fallback static table, mobile CSS and no-external-assets checks. |
| `pending` | `T10-CG-V2-M27..M30` evals/docs/future gates | Add fixture structural fields, search-quality eval loop, explicit future indexed-query/backend/semantic gates and final docs/source registry expansion beyond Batch 16. |
| `pending` | `T10-CG-V2-M31..M32` final verification and closure | Run focused/full verification, update final evidence and keep git staging/commit/push/PR explicit-only. |

## Deferred

| Status | Item | Reason |
| --- | --- | --- |
| `deferred` | Interactive dashboard editing | `status.html` remains a generated view; editing state in the dashboard would create a second source of truth. |
| `deferred` | Dashboard web server | Current scope is static offline HTML/JSON only; no standalone server or long-running process. |
| `deferred` | Live external telemetry widgets | External assets and external systems remain approval-bound and out of scope for the offline dashboard. |
| `deferred` | LLM semantic judge for question quality | Current transcript eval is deterministic term replay; calibrated judge coverage needs its own eval design and privacy policy. |
| `deferred` | Live Graphology/Sigma vendor bundle | Batch 16 records the local/vendor-only boundary and static fallback; adding vendored assets requires version, license, hash and visual QA evidence. |
| `deferred` | Project graph indexed-query backend | Static search index, local database/server or other indexed query backend remains outside the baseline until an approved design defines redaction, cache, eval threshold and rollback. |
| `deferred` | Project graph semantic extraction | LLM, embedding, cross-encoder, semantic rationale and comment extraction remain approval-gated future work, not implied by Batch 16 visual projection. |

## Verification

Batch 5 focused verification and Batch 6 full verification are recorded in `TEST.md` and `RUNLOG.md`.

Task 24 Batch 12 final verification is recorded in `TEST.md` and `RUNLOG.md`: focused docs/source-policy ran 23 tests with `OK`; full unittest ran 584 tests with `OK` in 551.714s, then reran after evidence notes and ran 584 tests with `OK` in 504.793s using `timeout_ms: 1200000`; fixture eval exited `0` for 85 fixture directories with `renderer_file_count: 191`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check and `git diff --check` exited `0`. The full unittest must continue to use `timeout_ms: 1200000` to avoid false timeouts on the current suite size.

Task 25 Batch 16 verification is recorded in `TEST.md` and `RUNLOG.md`: cockpit/visual/renderer RED checks failed before implementation on missing modules, focused cockpit suite ran 12 tests with `OK`, adjacent graph integration suite ran 60 tests with `OK` after reviewer-driven cockpit/visual/renderer hardening, Playwright visual smoke found 0 console errors after navigation, 0 external scripts, 8 pages, 14 nodes, 8 filters, selected-node evidence/filter behavior and no mobile horizontal overflow, full unittest ran 659 tests with `OK` in 698.951s using `timeout_ms: 1200000`, fixture eval exited `0` for 91 fixture directories with renderer file count 191 and 16 codex-runner fixtures, transcript eval exited `0` with 17 sessions and 0 failures, Codex compatibility returned `status: compatible`, docs check, strict MkDocs and `git diff --check` exited `0`. Commit, push and PR actions remain explicit-only.
