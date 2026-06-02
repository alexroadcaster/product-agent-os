# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-01

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Methodology applicability: gates are conditional and can be marked not applicable or accepted gap.
- Evidence-before-completion: implemented in `T8-A16`; no ready/completed/fixed/works/release claim without current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap.
- Architecture boundary: implementation stays inside named files and ownership boundaries.
- Domain traceability: complex domain work links domain model, bounded contexts, architecture boundary and ubiquitous language terms.
- Documentation quality: user-facing docs are Russian, behavior-level, and name inputs, outputs, verification, risks and next artifact.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive docs changes, or Codex compatibility regression.
- Accepted gap: allowed only when reason, owner, evidence owner and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and final response.

## Behavioral Route Evals

- Scenario workflows through `T8-S16`: implemented.
- No-placeholder planning, two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain model and bounded-context traceability: implemented.
- Ubiquitous language traceability: implemented in `T8-A7`.
- FSD structure routing: implemented in `T8-A8`.
- Metric hardening: implemented in `T8-A9`.
- Evidence-before-completion: implemented in `T8-A16`.
- Docs tooling selector and `docs_as_code_impact` applicability statuses: implemented in `T8-C`.
- Conditional readiness gates: implemented in `T8-F`.
- Scenario, behavioral eval and Codex compatibility docs: implemented in `T8-H`.
- Transcript/session eval replay: implemented in `T8-GY`.
- Standards trigger policy: implemented in `T8-B`.
- False-positive scenario fixture coverage: implemented in `T8-GX`.
- Detailed discovery status depth: implemented in `T8-D`.
- Track 9 methodology intelligence plan: authored in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Track 9 foundation, `T9-D1` Business/Product, `T9-D2` Requirements/Domain, `T9-D3` Solution Architecture, `T9-D4` Quality/Testing/Evals, `T9-D5` Codex/Agentic Workflow, `T9-D6` Frontend, `T9-D7` Backend, `T9-D8` API & Integrations, `T9-D9` Database & Data, `T9-D10` LLM / AI / RAG, `T9-D11` Security, Privacy & Compliance, `T9-D12` Delivery, Release & Operations, `T9-S` Task 20 Cross-Domain Synthesis and `T9-R` Task 21 Runtime Runner And Finish Options through `M25`: implemented.
- Track 10 guided questions and status dashboard: Task 23 `T10-Q-M15..M22` is implemented for fixture eval, lifecycle skill, behavioral/transcript eval, docs, README, source registry and root control-plane coverage; Batch 6 `T10-Q-M23..M25` full verification is complete.
- Track 10 self-verification and modernization loop: Task 24 Batch 12 docs/control-plane/final verification closure covers `T10-SV-M58..M62` for `agent_skill_metrics_loop` after focused source-priority, target-registry, evidence-intake, packet-bounds, trace-normalization, redaction-gate, dataset-quality, grader-summary, judge-calibration, metric-aggregation, repeatability, scorecard, confidence-gate, cadence, run-record, ledger, report, candidate, CLI, runtime, discovery, lifecycle, fixture, behavioral and transcript tests. Full unittest uses `timeout_ms: 1200000`; commit/push/PR remains explicit-only.
- Track 10 project code graph and HTML cockpit visualization: Task 25 Batch 13 `T10-CG-V2-M01..M07` is implemented for file-level graph foundation, Batch 14 `T10-CG-V2-M08..M13` is implemented for Python AST overlays and structured docs/contracts/schema/diagram overlays, Batch 15 `T10-CG-V2-M14..M18` is implemented for graph query packets, query CLI mode, runtime/status/lifecycle graph summaries and graph analysis reports, Batch 16 `T10-CG-V2-M19..M26` is implemented for generated cockpit visualization, Task 25 Batch 17 `T10-CG-V2-M27..M30` is implemented for fixture structural fields, search-quality eval loop, `project_graph_future_backend_semantic_gates_present` fixture coverage and future backend and semantic gates, Task 25 Batch 18 `T10-CG-V2-M31..M32` closes the baseline with focused/full verification, Task 25 Batch 19 `T10-CG-V2-M33..M38` implements the approved offline static search index after explicit user approval, Task 25 Batch 20 `T10-CG-V2-M39..M44` implements the approved local query backend/live database-server gate, Task 25 Batch 21 `T10-CG-V2-M45..M51` implements the approved semantic retrieval, embeddings and cross-encoder eval gate, Task 25 Batch 22 `T10-CG-V2-M52..M57` implements local deterministic LLM proposal generation and Task 25 Batch 23 `T10-CG-V2-M58..M62` implements future extension verification, rollback and closure. Batch 23 uses `project_graph_extension_closure.py`, `verify-extensions`, `disable-extensions`, rollback/data deletion proof, graph-only fallback and `blocked_without_new_explicit_approval` for live database/server, live external embedding/cross-encoder/LLM calls and canonical graph mutation. No live external model/API calls are allowed by Batch 23. git staging/commit/push/PR remains explicit-only.
- Batch 21 control-plane sync terms: `project_graph_semantic.py`, `project_graph_semantic_retrieval_gate_present`, semantic corpus and chunk policy, embeddings cache metadata, semantic query packets, cross-encoder eval, present_unverified orientation evidence, no canonical graph edge rewrites, later Batch 22/23 generated closure surfaces remain non-source-of-truth, and git staging/commit/push/PR remains explicit-only.
- Task 25 Batch 22 control-plane sync terms: `T10-CG-V2-M52..M57`, `project_graph_llm_extraction.py`, `project_graph_llm_extraction_gate_present`, `project_graph_llm_proposal_schema_present`, `project_graph_rationale_comment_proposals_present`, `project_graph_llm_extraction_eval_present`, prompt/model policy, staged proposals, not canonical graph facts, no canonical graph mutation, AI incident workflow, and git staging/commit/push/PR remains explicit-only.
- Task 25 Batch 23 control-plane sync terms: `T10-CG-V2-M58..M62`, `project_graph_extension_closure.py`, `project_graph_future_extension_closure_present`, `project_graph_extension_rollback_deletion_present`, `project_graph_unapproved_surface_blocking_present`, `project_graph_extension_full_verification_contract_present`, `verify-extensions`, `disable-extensions`, rollback/data deletion proof, graph-only fallback, `blocked_without_new_explicit_approval`, no live external model/API calls and git staging/commit/push/PR remains explicit-only.
- Task 26 Batch 24 control-plane sync terms: `T10-LIVE-M01..M06`, `project_graph_live_governance.py`, `project_graph_live_approval_packet_present`, `project_graph_live_data_classification_policy_present`, `project_graph_live_redaction_guard_present`, `project_graph_provider_credentials_boundary_present`, `project_graph_live_cache_deletion_policy_present`, `project_graph_live_budget_guard_present`, `project_graph_live_governance_no_live_calls_present`, no live server, no provider calls, no live external model/API calls, no canonical graph mutation, and git staging/commit/push/PR remains explicit-only.
- Task 25 Batch 17 compatibility terms remain preserved for historical docs/eval gates: semantic extraction and rationale/comment extraction stayed outside the Batch 17 baseline and required explicit approval with redaction, cache, token budget, eval threshold and rollback path before later approved generated proposal work.
- Batch 19 compatibility note: Task 25 Batch 19 `T10-CG-V2-M33..M38` used explicit user approval to add `project_graph_index.py`, `project_graph_static_search_index_present`, the offline static search index, generated, cache-bound and not source of truth behavior, graph artifact only source boundary and rollback/disable path.
- Batch 20 control-plane sync terms: project_graph_backend.py, project_graph_local_backend_gate_present, approval decision packet, storage path, port policy, process lifecycle, auth boundary, cleanup, logging, performance threshold and rollback path, disabled by default, generated local file-store, not source of truth, graph-only fallback, no production server.
- Task 25 Batch 16 `T10-CG-V2-M19..M26` remains the generated cockpit baseline with Code Flow inside `Code Intelligence`, Graphology-compatible static projection, local Graphology/Sigma vendor boundary and fallback static views.

## Track 9 Methodology Intelligence Evals

- Section protocol: every Track 9 section must start by reading its plan task and deeply auditing the matching `docs/methodologies/` source file.
- Plan freshness: if the source-file audit finds missing gates, artifacts, tooling candidates, false-positive risks, unsupported claims or open questions, the plan or Track 9 backlog must be updated before implementation.
- Domain coverage: every domain section must map source methodology concepts to catalog entries, discovery signals, readiness gates, artifact templates, lifecycle skill guidance, tests/evals and docs sync.
- Proportionality: DDD, FSD, docs portals, security/compliance, AI/RAG evals, database production gates and release governance must be conditional, with `not_applicable` or accepted gaps allowed when justified.
- Evidence: section completion requires focused tests/evals plus full verification proportional to touched files.
- Residual risk: semantic methodology quality still requires owner/domain/security/product review and cannot be proven by template presence alone.

## Runtime Runner Finish Option Evals

- `runtime_methodology_packet_present`: implemented through `T9-R-M25`.
- Required evidence: compact `methodology_packet`, bounded list/type validation, runtime route propagation, ordered `finish_options`, owner questions, source artifact ledger, semantic evidence sufficiency, safe next action and read-only methodology write policy.
- Approval boundary: recommendation-only packets cannot stage artifacts; high-risk methodology actions and external writes remain approval-required; automation promotion requires manual stability plus value/maturity evidence.
- Completion boundary: `present_unverified` methodology detections, recommendation text and source artifact presence do not satisfy completed/readiness claims without current verification evidence.
- Runtime safety checks: methodology route payloads are redacted, malformed packets return stable errors without traceback, and synthetic codex-runner fixtures cover approval, detection-only, external-write, automation maturity, redaction, malformed-packet, cross-domain bridge and compact first-response paths.
- Finish and ownership checks: CLI/validator JSON output, schema-v1 additive compatibility, lifecycle-status finish options, structured high-risk action taxonomy and ownership/parallelism rerouting are covered by focused unit tests and fixture eval checks.
- Residual risk: runtime checks prove the local contract shape and guard behavior for synthetic fixtures; they do not prove a real project's methodology evidence is semantically sufficient without owner review or an explicit accepted gap.

## Track 10 Guided Questions And Dashboard Evals

- Status: Task 23 guided question protocol and status dashboard is implemented and fully verified through Batch 6 `T10-Q-M23..M25`; commit/push remains explicit-only.
- Contract checks: typed `question_queue`, stable question IDs, one blocking question maximum in first response, bounded total question count, answer type validation, owner-question compatibility and no broad interview loops.
- Evidence checks: `answer_ledger` schema, stale-answer policy, private-data status, no secret-like values, status snapshot redaction, readiness/evidence summary and next safe action.
- Dashboard checks: offline `status.html`, no external URLs, safe embedded JSON, mobile-readable sections, stale evidence banner and generated-view-only source boundary.
- Fixture evidence: `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, and `stale_evidence_no_success_claim`.
- Behavioral/transcript cases: `guided-question-smallest-blocking-question`, `guided-question-no-broad-methodology-interview`, `status-dashboard-generated-view-only`, `status-dashboard-stale-evidence-no-success-claim`, and `runtime-first-response-no-question-dump`.
- Current verification evidence: full unittest ran 543 tests with `OK`; fixture eval exited `0` with `renderer_file_count: 187`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs and `git diff --check` exited `0`.
- Approval boundary: question ledgers, snapshots and dashboards are staged artifacts; they must not silently mutate a target workspace, activate hooks/automation or become a database/source of truth.
- Residual risk: guided questions and dashboards can structure progress, but they do not prove product decisions, implementation evidence or owner approvals are semantically sufficient for a real project.

## Track 10 Self-Verification And Modernization Evals

- Status: Task 24 Batch 12 docs/control-plane/final verification closure covers `T10-SV-M58..M62`, after Batch 7 `T10-SV-M-1..M4`, Batch 8 `T10-SV-M5..M16`, Batch 9 `T10-SV-M17..M28`, Batch 10 `T10-SV-M29..M45` plus guardrails `T10-SV-G4..G6`, and Batch 11 runtime/discovery/lifecycle/eval contracts through `T10-SV-M46..M57`.
- Task 24 Batch 12 closure requires Product-Agent OS docs, READMEs, source registry, Track 10 backlog and root control-plane artifacts to explain `agent_skill_metrics_loop`, target registry, trace intake, dataset quality, grader/judge calibration, cadence recommendation, scorecard ledger, report safety, modernization candidates, source-of-truth policy, staged evidence only, approval boundary, no live eval/model/API calls, no active schedules and no self-applied updates.
- Batch 7 focused evidence: source-priority policy accepts control-plane artifacts, run records, trace/eval packets and accepted gaps; rejects dashboard/report HTML, memory, raw chat logs and unsupported community claims; target registry collection is read-only; evidence intake marks stale, failed and accepted-gap evidence; metrics packets trim deterministically with warnings.
- Batch 8 focused evidence: trace intake normalizes Agents SDK, OpenTelemetry GenAI, tool-report and accepted-gap shapes; metrics redaction blocks scoring/report/candidate paths when unsafe raw prompts, tool output, local paths, secrets or private data appear; dataset builder keeps holdout/prior-failure/synthetic/flaky groups separate and reports duplicates/leakage; dataset quality gates block confident decisions with missing/leaky/low-sample data; grader summary remains local/metadata-only; judge calibration blocks candidate approval until calibrated.
- Batch 9 focused evidence: metric aggregation emits outcome, trajectory, harness reliability, harness optimizer, skill, cost/latency and safety sections with raw counts; repeatability calculates `pass@k`, `pass^k`, replay success and instability while blocking single lucky-run promotion; scorecards keep safety/false-pass/flake/trace/cost guardrails outside headline averages; confidence gates use Wilson lower bound and baseline delta; cadence remains suggested-only; run records redact evidence and reject dashboard-as-source claims.
- Batch 10 focused evidence: trace data-classification blocks unsafe trace data before scoring/reporting/candidate generation; offline report and dashboard rendering share a single generated-view-only/no-external-assets safety helper; scorecard ledger and daily/weekly packets remain Markdown/report artifacts; modernization candidates include priority, evidence and rollback gates; CLI supports dry-run/stage only; metrics-loop automation artifacts remain candidate-only.
- Batch 11 focused evidence: status snapshots include bounded metrics-loop summaries and staged report refs; discovery and methodology audit apply `agent_skill_metrics_loop` only to real agentic surfaces; runtime route packets validate bounded metrics-loop payloads and keep finish options review-only; guided questions keep one blocking owner question; lifecycle skills mark metrics-loop outputs as staged evidence only; fixture, behavioral and transcript coverage includes false-positive and abuse cases.
- Current verification evidence: Batch 12 focused docs/source-policy slice ran 23 tests with `OK`; full unittest ran 584 tests with `OK` in 551.714s, then reran after evidence notes and ran 584 tests with `OK` in 504.793s using `timeout_ms: 1200000`; fixture eval exited `0` for 85 fixture directories with `renderer_file_count: 191`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check and `git diff --check` exited `0`.
- Current fixture fields: `agent_skill_metrics_loop_contract_present`, `metrics_report_redacted`, `trace_normalization_contract_present`, `judge_calibration_gate_present`, `scorecard_ledger_contract_present`, `source_priority_contract_present`, `metrics_packet_bounds_present`, `trace_data_classification_gate_present`, `offline_artifact_safety_shared`, `no_baseline_renderer_pollution`, `active_metrics_automation_blocked`, `update_candidate_rollback_required`, `metrics_loop_runtime_route_contract_present`, `metrics_loop_lifecycle_contract_present` and `metrics_loop_false_positive_guards_present`.
- Remaining fixture fields before Task 24 closure: none for the local structural contract; real-project semantic sufficiency still requires owner review or accepted gaps.
- Required behavioral/transcript coverage: forbid headline-metric-only approval, self-applied updates, active automation, live eval calls, dashboard/report success claims, raw trace leakage, uncalibrated judge approval and update candidates without rollback.
- Source boundary: explicit control-plane artifacts, run records, trace/eval packets and accepted gaps are evidence; dashboard/report HTML, memory, raw chat logs and unsupported community claims are not source of truth.
- Approval boundary: self-verification can stage scorecards, reports and modernization candidates only; it cannot apply patches, mutate target workspaces, activate schedules, call live model/eval services or approve itself.
- Residual risk: Task 24 proves runtime/discovery/lifecycle/eval contract shape on top of the Batch 7-10 foundation and Batch 12 docs/control-plane closure. Owner review for real-project semantic metric sufficiency is still required.

## Track 10 Project Code Graph Evals

- Status: Task 25 Batch 23 `T10-CG-V2-M58..M62` implements future extension verification, rollback and closure on top of the Batch 13 graph foundation, Batch 14 scanner/overlay layer, Batch 15 query/runtime/analysis layer, Batch 16 generated cockpit, Batch 17 eval/future gates, Batch 18 focused/full verification closure, Batch 19 offline static search index, Batch 20 local backend gate, Batch 21 semantic retrieval gate and Batch 22 local deterministic LLM proposal gate. Batch 23 uses `project_graph_extension_closure.py` to build generated closure JSON at `.codex/product-agent-os/project-code-graph-extension-closure.json`, requires explicit verification evidence, records rollback/data deletion proof for generated Batch 19-23 artifacts, verifies graph-only fallback, blocks live database/server, live external embedding/cross-encoder/LLM calls and canonical graph mutation as `blocked_without_new_explicit_approval`, and is not source of truth. Runtime/status summaries, graph analysis reports, cockpit views, static index packets, backend store packets, semantic retrieval packets, LLM proposal packets and extension closure packets are orientation evidence only.
- Batch 23 verification evidence: focused Batch 23 module/CLI/fixture slice ran 6 tests with `OK`; Product-Agent OS docs contract suite ran 24 tests with `OK`; adjacent graph extension suite ran 50 tests with `OK`; full unittest ran 703 tests with `OK` in 724.475s using `timeout_ms: 1200000`; fixture eval exited `0` with renderer file count 191 and all emitted fixture records `ok: true`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch23_site` and `git diff --check` exited `0`.
- Required evidence before implementation closure: focused tests for graph schema, manifest/cache freshness, workspace/worktree provenance, observation lineage, edge invalidation/supersession, controlled ontology registry, partition scopes, canonical aliases, structured docs/contracts chunking, stage-local path/symlink safety, shrink guard, Python AST scanner, generated-file downranking, imports/calls, conservative symbol resolution, adapter extension points, heuristic dynamic-dispatch labels, docs/contracts/templates overlays, graph analysis, trace query, affected-test query, as-of/delta query, operation budget/tracing packets, adaptive token-budgeted graph queries, query filter safety, CLI dry-run/stage, status/runtime integration, cockpit information architecture, visual projection, local vendor manifest, Graphology-compatible export, Sigma bootstrap, selected-node evidence, graph navigation commands, fallback static view, mobile graph behavior, HTML renderer, Code Flow section, visual QA, search-quality evals, semantic/rationale extraction approval gating, no external assets, redaction and large-graph bounds.
- Required fixture fields: `project_code_graph_contract_present`, `project_graph_no_external_assets`, `project_graph_redaction_present`, `project_graph_scale_bounds_present`, `project_graph_generated_view_only`, `project_graph_manifest_freshness_present`, `project_graph_validation_and_shrink_guard_present`, `project_graph_query_budget_present`, `project_graph_code_flow_present`, `project_graph_provenance_guard_present`, `project_graph_observation_ledger_present`, `project_graph_temporal_delta_present`, `project_graph_ontology_registry_present`, `project_graph_structured_chunking_present`, `project_graph_alias_ledger_present`, `project_graph_operation_budget_present`, `project_graph_semantic_extraction_approval_required`, `project_graph_trace_query_present`, `project_graph_affected_tests_present`, `project_graph_search_quality_present`, `project_graph_static_search_index_present`, `project_graph_static_search_index_quality_present`, `project_graph_local_backend_gate_present`, `project_graph_backend_decision_packet_present`, `project_graph_backend_disabled_by_default`, `project_graph_backend_operational_controls_present`, `project_graph_backend_graph_only_fallback_present`, `project_graph_backend_no_production_or_source_truth_claims`, `project_graph_semantic_retrieval_gate_present`, `project_graph_semantic_retrieval_eval_present`, `project_graph_semantic_present_unverified_routing_present`, `project_graph_future_extension_closure_present`, `project_graph_extension_rollback_deletion_present`, `project_graph_unapproved_surface_blocking_present`, `project_graph_extension_full_verification_contract_present`, `project_graph_generated_file_downranking_present`, `project_graph_stage_safety_present`, `project_graph_visual_projection_present`, `project_graph_sigma_bootstrap_present`, `project_graph_visual_fallback_present`, `project_graph_selected_node_evidence_present` and `project_graph_visual_qa_present`.
- Batch 13 focused evidence: graph schema/ontology, file-level graph artifact, manifest freshness, observation lineage, CLI stage safety and graph safety tests ran 33 tests with `OK`; adjacent infrastructure renderer/CLI checks ran with the focused graph suite for 63 tests with `OK`.
- Batch 13 broad evidence: full unittest ran 617 tests with `OK` in 566.751s using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories including the six `project-code-graph-*` fixtures; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable site directory and diff hygiene exited `0`.
- Batch 14 focused evidence: scanner/overlay suite ran 14 tests with `OK`; focused graph suite ran 47 tests with `OK`; adjacent graph plus infrastructure renderer/CLI suite ran 77 tests with `OK`; reviewer agents reported no remaining spec or privacy/code-quality findings.
- Batch 14 broad evidence: full unittest ran 631 tests with `OK` in 554.103s using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories including the six `project-code-graph-*` fixtures; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable site directory and diff hygiene exited `0`.
- Batch 15 focused evidence: query/runtime/status/lifecycle focused suite ran 108 tests with `OK`, covering graph queries, query CLI mode, graph analysis, status snapshots, runtime contracts/routes, lifecycle skill source-of-truth wording and reviewer-driven regressions for budget/filter/path/unsupported-language behavior.
- Batch 15 broad evidence: full unittest ran 646 tests with `OK` in 558.013s using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories with renderer file count 191; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable site directory and diff hygiene exited `0`.
- Batch 16 focused evidence: cockpit/visual/renderer RED checks failed before implementation on missing modules; focused cockpit suite ran 12 tests with `OK`; adjacent graph integration suite ran 60 tests with `OK`; reviewer-driven regression coverage strips unsafe labels, local paths, external URLs and raw-source-like fields from visual projections, rejects unsafe cockpit Code Flow paths, allowlists analysis payloads, rejects manifest tampering, hard-caps visual limits, propagates renderer active page/section anchors and exercises working filter/navigation commands. Playwright visual smoke on staged cockpit HTML found 0 console errors after navigation, 0 external scripts, 8 pages, 14 nodes, 8 filters, selected-node evidence/filter behavior and no mobile horizontal overflow.
- Batch 16 broad evidence: full unittest ran 659 tests with `OK` in 698.951s using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories with renderer file count 191 and 16 codex-runner fixtures; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable site directory and diff hygiene exited `0`.
- Batch 17 focused evidence: search-quality RED failed before implementation on missing `project_graph_search_quality.py`; `python -m unittest tests.product_agent_os.test_project_graph_search_quality -v` then ran 2 tests with `OK`; fixture eval and docs sync add `project_graph_search_quality_present`, `project_graph_future_backend_semantic_gates_present`, fixture structural fields and explicit thresholds. The current Batch 17 eval remains local and deterministic, with no static search index, live database/server, LLM, embedding, cross-encoder, semantic extraction or rationale/comment extraction.
- Batch 17 broad evidence: adjacent graph/cockpit/search/docs suite ran 63 tests with `OK`; docs contract suite ran 17 tests with `OK` after restoring Batch 16 exact phrases; full unittest rerun ran 662 tests with `OK` in 671.629s using `timeout_ms: 1200000` after an earlier 662-test run exposed stale docs-contract wording; fixture eval exited `0` for 91 fixture directories with renderer file count 191; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch17_site` and `git diff --check` exited `0`.
- Batch 18 focused/full evidence: docs RED first exposed stale Batch 17 closure wording; graph/cockpit/search focused suite ran 70 tests with `OK`; status/runtime focused suite ran 47 tests with `OK`; fixture/lifecycle/docs suite ran 86 tests with `OK`; full unittest ran 664 tests with `OK` using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories with renderer file count 191; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch18_site` and `git diff --check` exited `0`; git staging/commit/push/PR remains explicit-only.
- Batch 19 focused and broad evidence: index/query/CLI/search-quality RED first exposed missing `product_agent_os.project_graph_index` and CLI `--build-index`; focused GREEN ran 27 tests with `OK`; adjacent graph/cockpit/index suite ran 78 tests with `OK`; fixture/lifecycle/docs suite ran 87 tests with `OK`; full unittest ran 673 tests with `OK` in 643.591s using `timeout_ms: 1200000`; fixture eval exited `0` with renderer file count 191 and all emitted fixture records `ok: true`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch19_site` and `git diff --check` exited `0`. Fixture eval adds `project_graph_static_search_index_present` and `project_graph_static_search_index_quality_present`; docs RED first exposed missing Batch 19 source registry, backlog, docs and root control-plane terms. Batch 19 proves generated offline cache schema, redaction, graph artifact only source boundary, optional indexed search, stale-index blocking, cache hit/miss/invalidation, explicit thresholds and rollback/disable path after explicit user approval.
- Batch 20 focused and broad evidence: backend/CLI RED first exposed missing `product_agent_os.project_graph_backend` and CLI `--build-backend`/`--backend-approval`; docs RED first exposed missing Batch 20 source registry, backlog, docs and root control-plane terms; focused GREEN ran 21 tests with `OK` across backend, CLI and fixture JSON output; docs contract suite ran 21 tests with `OK`; full unittest ran 680 tests with `OK` in 638.899s using `timeout_ms: 1200000`; fixture eval exited `0` with renderer file count 191 and all emitted fixture records `ok: true`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch20_site` and `git diff --check` exited `0`. Batch 20 proves explicit approval validation, malformed approval handling, generated local file-store schema, disabled-by-default server lifecycle, no production server, read-only API contract, stable JSON errors, performance/concurrency/rollback eval fields, graph-only fallback and fixture fields for local backend gate coverage.
- Batch 21 focused and broad evidence: semantic/CLI/fixture/docs RED first exposed missing `product_agent_os.project_graph_semantic`, missing CLI semantic index controls, missing fixture fields and stale docs/control-plane terms; focused GREEN ran 27 tests with `OK` across semantic retrieval, CLI, fixture renderer behavior, Batch 20 compatibility docs sync and Batch 21 docs/control-plane sync; docs contract suite ran 22 tests with `OK`; full unittest ran 688 tests with `OK` in 639.625s using `timeout_ms: 1200000`; fixture eval exited `0` with renderer file count 191 and all emitted fixture records `ok: true`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch21_site` and `git diff --check` exited `0`. Batch 21 proves explicit semantic approval validation, redacted semantic corpus/chunk policy, local deterministic embeddings and cross-encoder metadata, generated semantic retrieval cache, semantic query packets, stale graph-fingerprint blocking, semantic retrieval eval thresholds, `present_unverified` routing, no canonical graph edge rewrites and rollback/disable path.
- Batch 22 focused and broad evidence: LLM proposal/CLI/fixture/docs RED first exposed missing `product_agent_os.project_graph_llm_extraction`, missing CLI `--build-llm-proposals`/`--disable-llm-proposals`, missing fixture fields and stale docs/control-plane terms; focused GREEN ran 29 tests with `OK` across LLM extraction proposals, CLI, fixture renderer behavior, future matrix sync and Batch 22 docs/control-plane sync; docs contract suite ran 23 tests with `OK`; adjacent graph/backend/semantic/LLM suite ran 45 tests with `OK`; full unittest ran 697 tests with `OK` in 880.817s using `timeout_ms: 1200000`; fixture eval exited `0` for 91 fixture directories with renderer file count 191 and all emitted fixture records `ok: true`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check, strict MkDocs with disposable `.mkdocs_task25_batch22_site` and `git diff --check` exited `0`. Batch 22 proves explicit approval validation, local deterministic prompt/model policy, structured JSON proposal schema, semantic node and edge proposals, rationale/comment proposals, redaction/private-input blocking, unsupported-claim labels, human review decisions, AI incident workflow, stale semantic index blocking, cache hit/miss/invalidation, no canonical graph mutation and rollback/disable path.
- Future extension eval policy: Task 25 extension matrix `T10-CG-V2-M39..M62` now has Batch 20 implemented for local query backend/live database-server gate, Batch 21 implemented for local deterministic semantic retrieval with embeddings/cross-encoder eval, Batch 22 implemented for local deterministic LLM semantic extraction/rationale-comment proposals and Batch 23 implemented for future extension verification, rollback and closure. Batch 22 outputs are staged proposals, not canonical graph facts. Batch 23 outputs are generated closure evidence only; live production server, live external model/API providers and canonical graph mutation remain `blocked_without_new_explicit_approval`. Planning matrix presence is not implementation evidence.
- Scale/search evals: 1k, 5k and 10k node fixtures prove bounded summaries, top-N subgraphs, adaptive token-budgeted traversal, hub suppression, clustering/level-of-detail policy, community quality controls, large-graph visual render modes, fallback usability and no full graph prompt dump. Batch 17 search-quality evals cover symbol recall, top-k/MRR, trace failure labeling, affected-test precision, explicit thresholds and edge density; delta/as-of query bounds and operation-budget reporting remain covered by existing query packets rather than a live backend.
- Source boundary: code/docs plus graph JSON/JSONL/manifest/report artifacts are evidence; HTML graph and Code Flow pages are generated review output; unsupported languages, inferred edges and ambiguous dependencies must be visibly labelled.
- Residual risk: Task 25 can improve navigation and agent read-order, but dependency graphs can still miss dynamic behavior, runtime wiring, framework conventions, real production dispatch paths and semantic meaning of domain concepts without owner review, current source reads or accepted gaps.

## Business Product Evals

- `business_product_contract_present`: implemented in `T9-D1`.
- Required evidence: product hypothesis, target segment, value proposition, opportunity framing, decision horizon, metric scope, analytics tracking plan, qualitative feedback loop, privacy classification, AI product eval where applicable, release measurement evidence and workflow-promotion value evidence.
- False-positive protection: typo-only docs edits, formatting-only edits and dependency pins without behavior impact do not force product methodology.
- Residual risk: product artifacts prove the evidence shape, not that the selected market, value proposition or metric is strategically correct.

## Requirements Domain Evals

- `requirements_domain_contract_present`: implemented in `T9-D2`.
- Required evidence: requirements scope, requirements owner, requirement quality, stable IDs, acceptance scenarios, declarative scenario quality, requirements traceability, business rules, non-goals/constraints, constraints traceability, open questions, stakeholder owner map, story slice map, Example Mapping, domain discovery, domain model when complex, bounded context trace, ubiquitous language trace, invariants/failure modes, domain event contracts, API/UI/data traceability, domain expert review, requirement change impact, accepted gap and requirements evidence before implementation.
- False-positive protection: typo-only docs edits, formatting-only edits and dependency metadata without behavior impact do not force Requirements & Domain methodology on README-only work.
- Unsupported claims rejected: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language and OpenAPI is requirements source of truth.
- Residual risk: requirements/domain artifacts prove traceability structure, not that domain experts have semantically validated every business rule.

## Solution Architecture Evals

- `solution_architecture_contract_present`: implemented in `T9-D3`.
- Required evidence: architecture scope, C4 context/container or equivalent boundary map, slice boundary, boundary responsibility owner, bounded-context-to-architecture trace, dependency rules, public contract trace, data ownership boundary, runtime topology, observability architecture, quality attribute scenarios, ADR/tradeoff record, trust boundary review, diagram render check, architecture fitness functions, migration rollback path, architecture docs lifecycle, owner review and accepted gaps.
- False-positive protection: typo-only docs edits, formatting-only edits, docs-light prototypes without reviewed/diffable diagrams and non-cloud work without Well-Architected review do not force Solution Architecture methodology.
- Unsupported claims rejected: architecture means diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves architecture quality, architecture-as-code is always required and AI can design architecture from chat alone.
- Residual risk: architecture artifacts prove boundary and evidence shape, not that the selected architecture is semantically optimal or owner-approved for a real production system.

## Quality Testing Evals

- `quality_testing_evals_contract_present`: implemented in `T9-D4`.
- Required evidence: quality strategy, risk based scope, test-first evidence or explicit gap, acceptance traceability, contract checks, runtime evidence, manual QA evidence, visual/a11y evidence, eval spec, eval rerun evidence, current evidence before completion, CI quality gate, flaky-test policy, coverage policy, test data privacy, bug reproduction evidence and regression impact.
- False-positive protection: typo-only docs edits, formatting-only edits, docs-only source cleanup and dependency metadata changes without behavior impact do not force Quality, Testing & Evals methodology.
- Unsupported claims rejected: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate because they are most realistic, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Residual risk: quality artifacts prove current evidence shape and gate routing, not that a human owner has judged every check sufficient for the real project risk.

## Codex Agentic Workflow Evals

- `codex_agentic_workflow_contract_present`: implemented in `T9-D5`.
- Required evidence: agentic scope, project source of truth, control plane, read-only discovery, approval boundary, fresh-context handoff, ownership split, subagent parallelism safety, skill promotion evidence, plugin boundary, MCP permission review, hook activation approval, automation manual stability, model/reasoning policy, memory policy, agent eval workflow and evidence before completion.
- False-positive protection: simple docs/local work does not force subagents, worktrees, MCP review, hook governance, plugin packaging, automation, Agents SDK orchestration or agent eval workflow unless signals, intent or side-effect risk make them applicable.
- Unsupported claims rejected: memory is project source of truth, subagents are automatically faster, MCP tools are safe because they are tools, hooks are harmless convenience scripts, repeated workflows should become automation immediately, Agents SDK and Codex runtime are the same layer, and inspection proves completion.
- Residual risk: Codex workflow artifacts prove governance shape and approval routing, not that a human owner has approved every model, subagent, MCP, hook, skill, plugin or automation decision for a real project.

## Frontend Evals

- `frontend_contract_present`: implemented in `T9-D6`.
- Required evidence: user-flow acceptance, component docs, component state matrix, design-system boundary, conditional FSD boundary review, API/data state alignment, accessibility review, keyboard/focus contract, responsive viewport matrix, visual evidence, browser/runtime evidence, console status, Playwright trace or accepted gap, performance budget, browser support, content/i18n boundary and interaction test evidence.
- False-positive protection: backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD work does not force Frontend methodology.
- Unsupported claims rejected: FSD is mandatory for every frontend project, Storybook proves UI quality, automated accessibility addon output is enough, a desktop screenshot proves responsive UI, lab Web Vitals always represent production UX and code inspection proves UI completion.
- Residual risk: frontend artifacts prove UI evidence shape and route/gate coverage, not that a human owner has semantically accepted every screenshot, interaction test, accessibility review or performance budget as sufficient for a real product.

## Backend Evals

- `backend_contract_present`: implemented through `T9-D7-M45`.
- Required evidence: service/module boundary, owner, inbound contracts, outbound dependencies, data ownership, deployment/runtime shape, runtime behavior, dependency failure matrix, observability, SLI/SLO or explicit gap, health endpoint semantics, job/queue contract, data consistency strategy, config/secrets boundary, security review, rollback/recovery and owner-reviewed evidence sufficiency or accepted gap.
- Resilience depth: remote dependencies record per dependency timeout, retry/backoff/max attempts, circuit breaker non-applicability, fallback, alert owner and verification evidence.
- Jobs and data depth: queues/jobs record payload contract, retry policy, dead-letter behavior, dead-letter queue, idempotency key, replay procedure, poison-message handling, deduplication, ordering and backpressure; risky distributed data behavior records local transaction, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path.
- Operations depth: observability rejects logs-only evidence and requires traces, metrics, logs, dashboards, alerts, correlation IDs, alert ownership, redaction and no-private-payload logging; health checks distinguish liveness, readiness, startup and platform equivalents.
- Rollback and boundary depth: risky backend changes record rollback command or manual procedure, data recovery/replay, irreversible side effects, owner approval and residual risk; new or changed backend responsibility records owner review, decision authority, boundary rationale and ADR link or accepted gap.
- Twelve-Factor depth: backend templates use Twelve-Factor vocabulary for explicit dependencies, config/env keys, build-release-run, process model, stateless process or accepted gap, admin tasks, dev/prod parity and logs-as-event-stream without making Twelve-Factor a mandatory framework.
- Intake/security/ops/contract depth: backend requirements intake records service/user behavior, affected backend unit, dependencies, data stores, runtime constraints, operational assumptions and explicit gaps before implementation planning; security notes cover authn/authz, secrets, rate limits, audit logging, sensitive data, abuse cases, privileged operations and no-secrets evidence.
- Discovery depth: backend dependency categories are exposed as `present_unverified` signals for database, message broker, cache, payment, email, storage, search and third-party HTTP/provider clients; backend delivery discovery records backend stack, backend commands, CI, APIs, DB, queues, workers, deployment manifests and security signals without executing deployments or external writes.
- Severity and snippet policy: risky production backend without service boundary/runtime/failure evidence/security route/rollback is blocker/high-risk; complete accepted-gap fields downgrade eligible observability/SLO/health recommendations; simple local/backend-light work stays warning-level. T9-D7 templates stay framework-agnostic and defer Node.js, Python, Java, .NET and Go snippets until stack-specific owner/examples/verification exist.
- Retry/idempotency detection: T9-D7 uses lightweight read-only signals for retry/idempotency terms plus dependency/job context; deeper static analysis of correctness is deferred to avoid false positives.
- Evidence sufficiency routing: backend records owner reviewed test/eval/runtime evidence sufficiency for real project risk or accepted gap owner, reason, review date, downstream risk and follow-up; shared semantic sufficiency normalization remains T9-S/cross-domain.
- False-positive protection: frontend-only, docs-only, CLI-only, native-only, dependency metadata without backend runtime behavior and package-name-only service folders do not force Backend methodology.
- Unsupported claims rejected: backend means only business logic files, microservices are the professional default, retries make systems reliable, health endpoint exists so readiness is solved, logs are observability and SLOs are only for large companies.
- Residual risk: backend artifacts prove evidence shape and route/gate coverage, not that a human owner has judged runtime tests, SLOs, health checks, rollback plans, operational runbooks or provider contracts sufficient for a real production system.

## API Integrations Evals

- `api_integrations_contract_present`: implemented in `T9-D8`.
- Required evidence: source-of-truth contract, consumer map, compatibility/breaking-change review, security schemes/scopes/token claims/object-level authorization/rate limits, error contract, contract-test matrix, event/webhook delivery contract, generated SDK manifest, external-write approval, request ID, correlation ID, API observability, style choice and unsupported API claim rejection.
- False-positive protection: Swagger UI/rendered docs alone does not make an API contract source, API-only contract fixtures do not force Backend blockers, internal APIs can still have consumers, and GraphQL/gRPC/events are not universal defaults.
- Unsupported claims rejected: Swagger UI is source of truth, schema validation is contract testing, OAuth proves API security, GraphQL/gRPC/events are mandatory defaults and internal APIs have no consumers.
- Residual risk: API artifacts prove contract evidence shape and route/gate coverage, not that a human owner has judged every consumer, compatibility rule, authz rule, error semantic, event delivery policy, generated SDK release or external-write approval sufficient for a real production system.

## Database Data Evals

- `database_data_contract_present`: implemented in `T9-D9`.
- Required evidence: database inventory, database dictionary, schema source, migration plan, expand-contract rollout, transaction boundary, rollback feasibility, backup/restore evidence, data classification, data quality checks, producer/consumer data contract, lineage, query/index performance, retention/deletion policy, synthetic fixture policy, production access approval, constraints/integrity and unsupported database claim rejection.
- False-positive protection: schema-only files and local/demo database fixtures stay `present_unverified`; runtime pipeline and RAG ingestion signals stay `present_unverified` until owner-reviewed runtime, lineage or ingestion evidence exists.
- Approval boundary: DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation remain `approval_required`.
- Unsupported claims rejected: ORM schema is database source of truth, migration applied means safe, down migration means rollback-safe, backups exist means restore-safe, manual SQL is enough, anonymized production data is safe by default and lineage can be reconstructed later.
- Residual risk: database artifacts prove evidence shape and route/gate coverage, not that a human owner has accepted migration safety, data quality, rollback, restore, lineage, privacy or production-access sufficiency for a real production system.

## LLM AI RAG Evals

- `llm_ai_rag_contract_present`: implemented through `T9-D10-M36`.
- Required evidence: AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, dataset governance, prompt contract, model decision record, structured output schema, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding rubric, agent task packet, agent workflow trace, guardrail matrix, trace evidence packet, cost/latency budget and current-run evidence before AI/RAG quality claims.
- Tooling and migration depth: eval tooling selector records Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas and LangSmith as conditional choices with selected/rejected/deferred runner rationale; model migration records snapshot or approved alias, prompt migration impact, compatibility checks, rollback, minimum threshold and sampling parameter rationale.
- RAG lifecycle and incident depth: RAG source/retrieval/dataset artifacts record deletion path, retention, source exclusion, stale-source pruning, privacy owner, vector store lifecycle, deletion propagation, deduplication and privacy review; failed eval, hallucination report, unsafe output, tool misuse or data exposure routes to an AI incident workflow with severity, mitigation, follow-up eval and Security/Privacy handoff.
- Discovery/report depth: AI behavior diff signals are limited to workspace and intent signals with no external branches or network dependency; methodology reports render evidence_required, approval_boundary, accepted_gap_option, residual_risk and safe_next_action with redaction.
- False-positive protection: docs-only AI mentions, generic context maps, generic tools, generic schemas, frontend `model/` folders, vector math and non-behavior prompt documentation do not force AI/RAG methodology blockers.
- Approval boundary: live model calls, external eval services, vector DB access, raw prompt/trace/customer-data review, tool writes, shell/money/data exposure and irreversible side effects remain approval-bound.
- Unsupported claims rejected: prompt inspection is enough, citations alone prove grounding, model upgrade automatically improves quality, schema presence proves tool safety and AI quality can be claimed without current eval evidence.
- Residual risk: AI/RAG artifacts prove evidence shape and route/gate coverage, not that a human owner has judged eval thresholds, prompts, model choice, grounding quality, tool permissions, guardrails or cost/latency budgets sufficient for a real production system.

## Security Privacy Compliance Evals

- `security_privacy_compliance_contract_present`: implemented in `T9-D11`.
- Required evidence: security-sensitive classification, threat surface, security risk review, ASVS/SSDF/SAMM mapping, ASVS level selection, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact record, external-write approval, abuse/rate-limit review, audit logging review, supply-chain review, SBOM/provenance decision, CI permissions, AI security review, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status and security evidence before completion.
- False-positive protection: docs-only security articles, keyword-only compliance claims, package metadata, SBOM files and CI permission files stay `present_unverified` until owner-reviewed evidence exists; docs-only repositories do not become regulated automatically.
- Approval boundary: payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes, publish actions and Codex Security scans remain approval-bound or explicitly not requested.
- Unsupported claims rejected: security review after coding, no-secrets-in-code means safe, ASVS/OWASP proves compliance, SBOM once is enough, Codex Security scan is implied, OAuth proves API security and privacy compliance is universal.
- Residual risk: security/privacy/compliance artifacts prove evidence shape and route/gate coverage, not legal compliance, certification, or that a human security/privacy/compliance owner has accepted every residual risk for a real production system.

## Delivery Release Operations Evals

- `delivery_release_operations_contract_present`: implemented in `T9-D12`.
- Required evidence: release scope, version impact, changelog/release notes, artifact manifest, release evidence before completion, rollout strategy, rollback/recovery, environment approval boundary, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review, automation manual stability, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency.
- False-positive protection: docs-only release notes, CI-only workflows, deployment manifests without execution, feature flags without owners, GitOps files without approval paths, mobile signing alone, DORA individual quota and release/observability tooling files without owner evidence stay insufficient for release-ready claims.
- Approval boundary: publish, tag, GitHub Release creation, artifact upload, deploy, PR creation, branch push, package registry mutation, marketplace/store submission, CI/CD environment mutation and active automation remain `approval_required`.
- Unsupported claims rejected: CI green means release ready, tests passed so release is ready, rollback is just revert, feature flags remove release risk, GitOps is automatically safe, generated changelog is enough for users, DORA metrics prove individual performance and repeatable automation is automatically safe.
- Residual risk: delivery/release/operations artifacts prove evidence shape and route/gate coverage, not that a human release, operations, security or product owner has accepted every release risk for a real production system.

## Cross Domain Synthesis Evals

- `cross_domain_synthesis_contract_present`: implemented through `T9-S-M14`.
- Required evidence: grouped recommendations, owner domains, consumer domains, source domains, merged gates, source artifact ledger, alias/deferred artifact decisions, semantic evidence sufficiency, owner-question dedupe, risk-aware safe next action and lifecycle skill consumption.
- Fixture evidence: `run_fixture_eval.py` exposes `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present`.
- False-positive protection: small PII, complex non-production monorepo, internal CLI, docs-only release notes, CI-only workflows, tooling-only release files and backend FSD-like directories do not force unrelated heavy methodology gates without owner-reviewed evidence.
- Approval boundary: synthesized recommendations stay read-only/staged; detection alone remains `present_unverified` and does not authorize scaffolding, external writes, release actions, production access, security scans, automations or finish claims.
- Residual risk: synthesis artifacts prove packet shape, grouping and routing, not that a human owner has accepted every real-project overlap or evidence sufficiency decision.

## Completion Evidence Evals

- `evidence_before_completion`: implemented in `T8-A16`.
- Required evidence: ready claim, completed claim, fixed claim, works claim and release claim need current command evidence, current eval evidence, current runtime evidence or explicit test gap.
- Inspection-only: answers based only on code inspection must stay labeled `inspection-only` and list unsupported completion claim.
- Residual risk: the gate proves evidence is recorded, not that manually interpreted evidence is semantically sufficient.

## Domain Model Evals

- `domain_model_when_complex_domain`: implemented in `T8-A5`.
- `bounded_context_architecture_boundary_trace`: implemented in `T8-A6`.
- `ubiquitous_language_traceability`: implemented in `T8-A7`.
- Human domain/architecture review remains required for conceptual correctness.

## UI Architecture Evals

- `fsd_structure`: implemented in `T8-A8`.
- False-positive protection: backend, native, simple CRUD and simple MVP work must not be forced into Feature-Sliced Design.
- Residual risk: directory detection does not prove architecture quality; owner review is still required for public API and import rule correctness.

## Metric Hardening Evals

- `metric_hardening_when_product_behavior_changes`: implemented in `T8-A9`.
- Required evidence: North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence.
- Residual risk: metric artifacts reduce proxy-metric and telemetry risk, but a product owner still needs to validate whether the selected metric actually reflects user value.

## Docs Tooling Evals

- `docs_tooling_selector`: implemented in `T8-C`.
- `docs_as_code_impact`: supports `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: selected tools, rejected tools, evidence owner, maintenance owner, commands, accepted gap or approval boundary.
- False-positive protection: docs-light and internal-only projects are not forced into MkDocs, Docusaurus, Sphinx, Antora, hosted docs, CI activation or DB introspection.
- Residual risk: selector evidence is route and artifact evidence; owners still need to validate whether a chosen docs tool is operationally worth maintaining.

## Conditional Readiness Evals

- `conditional_readiness_gates_contract_present`: implemented in `T8-F`.
- `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: every gate has `applies_when`, pass condition, accepted gap, required evidence, owner and residual risk.
- False-positive protection: detection alone can only support `present_unverified`; applicable gates without evidence are `applicable_missing`, not ready.
- Residual risk: the contract proves readiness evidence is structured; owners still need to judge whether the evidence is sufficient for the actual project risk.

## Scenario Documentation Evals

- `test_product_agent_os_docs`: implemented in `T8-H`.
- Required evidence: dedicated scenario, behavioral eval and Codex compatibility pages have Source status, Inputs, Outputs, Verification and Risks.
- Navigation evidence: MkDocs nav and `tools/check_docs.py` required paths include the new pages.
- Residual risk: docs describe route and eval contracts; transcript/session replay catches deterministic term/shortcut/privacy failures but does not replace semantic reviewer judgment.

## Transcript Session Evals

- `evaluate_transcript_sessions`: implemented in `T8-GY`.
- Required evidence: each synthetic or redacted session maps to `behavioral_case`, has `expected_terms`, optional `forbidden_terms`, and produces `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`.
- Runner evidence: `run_transcript_eval.py` exits `0` only when every session passes and exits `1` when expected evidence is missing, forbidden behavior appears or unsafe transcript content is retained.
- Residual risk: deterministic replay is stable and local, but it is not a calibrated LLM-as-judge for nuanced conversation quality.

## Standards Trigger Evals

- `standards_trigger_policy`: implemented in `T8-B`.
- Required evidence: ADR trigger policy, C4/arc42 applicability, OpenAPI source of truth, AsyncAPI event contract, SemVer impact, Keep a Changelog categories, CODEOWNERS status, GitHub Actions least privilege, `governance-proposal.md` and no forced external activation.
- Fixture evidence: `standards_trigger_contract_present` in `run_fixture_eval.py`.
- Residual risk: the contract proves standards applicability is recorded; owners still need to decide whether an ADR, diagram, governance proposal or release category is proportionate for the real project.

## False-Positive Fixture Evals

- `T8-GX`: implemented.
- Required evidence: `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal` and `hosted-docs-approval` are synthetic, secret-free fixtures with named expected checks in `run_fixture_eval.py`.
- Fixture evidence: `fsd_structure_not_detected_for_backend`, `fsd_structure_not_detected_for_native`, `domain_model_not_forced_for_simple_crud`, `docs_light_does_not_select_heavy_portal` and `hosted_docs_and_db_introspection_require_approval`.
- Residual risk: false-positive fixtures prove routing boundaries for selected synthetic workspaces; they do not prove every real project-specific methodology decision.

## Detailed Discovery Status Evals

- `T8-D`: implemented.
- Required evidence: `methodology_applicability` is present in discovery output with packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision and standards trigger policy.
- Fixture evidence: `methodology_applicability_contract_present` in `run_fixture_eval.py`.
- Residual risk: discovery packets structure methodology/tooling applicability; owners still need to validate semantic quality and sufficiency of the evidence for the real project.

## Task 22 final documentation sync closure

- Eval target: Task 22 final documentation sync closure proves user-facing docs, READMEs, source registry and root control-plane files describe implemented Track 1-9 behavior instead of planned or stale claims.
- readiness/evidence quality: docs must preserve `present_unverified` versus `present_verified`, approval_required boundaries, owner-reviewed evidence sufficiency and evidence-before-completion language.
- stale Track 1-9 claims: docs must not reintroduce standalone Agents SDK runtime, live model/API calls, hidden MCP/hook/automation activation, direct target-workspace writes, or the obsolete Track 9 Task 23 final baseline as the next implementation task.
- synthetic eval evidence limits: fixture evals, docs tests and transcript/session replay prove deterministic route and docs contracts, but they do not prove real project readiness without current command evidence, runtime evidence, owner evidence or explicit accepted gaps.
- Current Task 22 eval evidence: focused docs tests ran 13 tests with `OK`; fixture eval exited `0` with 80 fixtures, 0 failures and renderer file count 186; transcript eval exited `0` with 5 sessions and 0 failures; full unittest ran 520 tests with `OK`; Codex compatibility returned `status: compatible`; docs, strict MkDocs and diff hygiene exited `0`.
- Residual risk: Task 22 is documentation/source-registry closure; it does not add runtime behavior, dashboard behavior or Track 10 guided-question implementation.

## Unsupported Claims

- Claim:
- Missing source:
- Verification needed:
<!-- product-agent-os:end evals -->
