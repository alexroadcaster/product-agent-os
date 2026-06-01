# TEST.md

<!-- product-agent-os:start test-plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-01

## Current Baseline

- Track 10 Task 25 Batch 17 status: `T10-CG-V2-M27..M30` is implemented for fixture structural fields, a search-quality eval loop, `project_graph_future_backend_semantic_gates_present` fixture coverage and future backend and semantic gates. Batch 17 records symbol recall, top-k/MRR, trace labels, affected-test precision, edge density and explicit thresholds. The static search index, live database/server, LLM, embedding, cross-encoder, semantic extraction and rationale/comment extraction remain outside the baseline unless explicit approval defines redaction, cache, token budget, eval threshold and rollback path. Batch 18 remains for final Task 25 closure, and git staging/commit/push/PR remains explicit-only.
- Task 25 Batch 16 `T10-CG-V2-M19..M26` remains the generated cockpit baseline with Code Flow inside `Code Intelligence`, Graphology-compatible static projection, local Graphology/Sigma vendor boundary, selected-node evidence and fallback static views.
- Track 10 Task 25 Batch 13 RED evidence: `python -m unittest tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety -v` failed before implementation on missing `product_agent_os.project_graph_ontology`, `project_code_graph`, `project_graph_manifest`, `project_graph_observations` and missing `scan_project_code_graph.py`.
- Track 10 Task 25 Batch 13 focused GREEN evidence: the same focused suite ran 33 tests with `OK` after addressing spec/code review findings for temporal delta artifacts, git provenance/build metadata including linked worktree `.git` files, observation-reference validation, docs-heavy fixture coverage, scale fixture directories, symlink escapes, edge-ID collisions, nested raw-source keys, stage payload/error path redaction, generic filesystem error path redaction, backup before normal staged overwrite, capped line counting and bounded file collection with omitted counts.
- Track 10 Task 25 Batch 13 adjacent staging/renderer check: `python -m unittest tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety tests.product_agent_os.test_infrastructure_renderer tests.product_agent_os.test_render_infrastructure_cli -v` ran 63 tests with `OK`.
- Track 10 Task 25 Batch 13 broad verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 617 tests with `OK` in 566.751s using `timeout_ms: 1200000`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` for 91 fixture directories including six `project-code-graph-*` fixtures and `renderer_file_count: 191`; `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 17 sessions and 0 failures; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Track 10 Task 25 Batch 13 docs/build/diff hygiene: `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_batch13_site` exited `0`; disposable `.mkdocs_task25_batch13_site` was removed; `git diff --check` exited `0`.
- Track 10 Task 25 Batch 14 RED evidence: `python -m unittest tests.product_agent_os.test_project_graph_python_scanner tests.product_agent_os.test_project_graph_overlays -v` failed before implementation on missing `product_agent_os.project_graph_adapters` and `product_agent_os.project_graph_chunking`.
- Track 10 Task 25 Batch 14 focused GREEN evidence: scanner/overlay suite ran 14 tests with `OK`; focused graph suite ran 47 tests with `OK`; adjacent graph plus infrastructure renderer/CLI suite ran 77 tests with `OK` after reviewer-driven fixes for dotted absolute imports, fixture/eval-fixture links, standalone PlantUML, path-sensitive aliases, explicit worktree partition scope, missing imported-symbol fallback, duplicate edge/heading IDs, bounded file reads, source-derived secret/local-path redaction and direct Markdown local-path link filtering.
- Track 10 Task 25 Batch 14 broad verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 631 tests with `OK` in 554.103s using `timeout_ms: 1200000`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` for 91 fixture directories including six `project-code-graph-*` fixtures and `renderer_file_count: 191`; `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 17 sessions and 0 failures; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Track 10 Task 25 Batch 14 docs/build/diff hygiene: `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_batch14_site` exited `0`; disposable `.mkdocs_task25_batch14_site` was removed; `git diff --check` exited `0`.
- Track 10 Task 25 Batch 15 RED evidence: focused query/runtime/status/lifecycle suite failed before implementation on missing `product_agent_os.project_graph_queries`, missing `product_agent_os.project_graph_analysis`, missing `validate_project_graph_status_packet`, missing `scan_project_code_graph.py --query`, missing status snapshot graph summaries, missing `plan_route(project_graph_status=...)` and missing lifecycle skill project graph wording.
- Track 10 Task 25 Batch 15 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_project_graph_queries tests.product_agent_os.test_project_graph_analysis tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_lifecycle_skills -v` ran 108 tests with `OK` after reviewer-driven fixes for query-specific budget enforcement, graph filter enum validation, runtime graph-ref path safety, unsupported-language packet shape, unresolved-call analysis and low-severity route behavior.
- Track 10 Task 25 Batch 15 broad verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 646 tests with `OK` in 558.013s using `timeout_ms: 1200000`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` for 91 fixture directories with renderer file count 191; `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 17 sessions and 0 failures; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Track 10 Task 25 Batch 15 docs/build/diff hygiene: `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_batch15_site` exited `0`; disposable `.mkdocs_task25_batch15_site` was removed; `git diff --check` exited `0`.
- Track 10 Task 25 Batch 16 RED evidence: `python -m unittest tests.product_agent_os.test_project_cockpit_model tests.product_agent_os.test_project_graph_visual_model tests.product_agent_os.test_project_graph_renderer -v` failed before implementation on missing `product_agent_os.project_cockpit_model`, `product_agent_os.project_graph_visual_model` and `product_agent_os.project_graph_renderer`.
- Track 10 Task 25 Batch 16 focused GREEN evidence: the same cockpit/visual/renderer suite ran 12 tests with `OK` after reviewer-driven fixes for visual projection sanitization, unsafe cockpit Code Flow paths, analysis payload allowlisting, manifest tamper rejection, hard visual caps, renderer active page/section anchor propagation and working filter/navigation commands.
- Track 10 Task 25 Batch 16 adjacent graph check: `python -m unittest tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_graph_overlays tests.product_agent_os.test_project_graph_analysis tests.product_agent_os.test_project_graph_queries tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety tests.product_agent_os.test_project_cockpit_model tests.product_agent_os.test_project_graph_visual_model tests.product_agent_os.test_project_graph_renderer -v` ran 60 tests with `OK`.
- Track 10 Task 25 Batch 16 visual QA smoke: staged cockpit HTML was served locally and checked with Playwright; after navigation it had 0 console errors, 0 external scripts, 8 cockpit pages, 14 graph nodes, 8 filters, selected-node evidence/filter behavior and no mobile horizontal overflow at 390px width.
- Track 10 Task 25 Batch 16 broad verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 659 tests with `OK` in 698.951s using `timeout_ms: 1200000`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` for 91 fixture directories with renderer file count 191 and 16 codex-runner fixtures; `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 17 sessions and 0 failures; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Track 10 Task 25 Batch 16 docs/build/diff hygiene: `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_batch16_site` exited `0`; disposable `.mkdocs_task25_batch16_site` was removed; `git diff --check` exited `0`. A first strict MkDocs attempt without the project MkDocs `PYTHONPATH` failed because the default Python environment did not include `mkdocs`; the successful rerun used the project-local MkDocs path.
- Track 10 Task 25 Batch 17 RED evidence: `python -m unittest tests.product_agent_os.test_project_graph_search_quality -v` first failed before implementation on missing `product_agent_os.project_graph_search_quality`; fixture eval first exposed absent Batch 17 fixture structural fields and missing `project_graph_future_backend_semantic_gates_present`; docs RED coverage first exposed missing Task 25 Batch 17 source registry, backlog and control-plane terms.
- Track 10 Task 25 Batch 17 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_project_graph_search_quality -v` ran 2 tests with `OK`; the implemented local search-quality eval loop records symbol recall, top-k/MRR, trace labels, affected-test precision, edge density and explicit thresholds without raw source bodies or live backend/model calls. Focused fixture/docs checks for fixture structural fields, search-quality eval loop and future backend and semantic gates are part of the current Batch 17 verification run.
- Track 10 Task 25 Batch 17 adjacent graph/docs check: `python -m unittest tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_graph_overlays tests.product_agent_os.test_project_graph_analysis tests.product_agent_os.test_project_graph_queries tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety tests.product_agent_os.test_project_cockpit_model tests.product_agent_os.test_project_graph_visual_model tests.product_agent_os.test_project_graph_renderer tests.product_agent_os.test_project_graph_search_quality tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track10_task25_project_graph_batch17_docs_and_control_plane_are_synced -v` ran 63 tests with `OK`.
- Track 10 Task 25 Batch 17 docs contract check: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 17 tests with `OK` after restoring backward-compatible Batch 16 documentation terms required by the existing docs contract.
- Track 10 Task 25 Batch 17 broad verification: `python -m unittest discover -s tests -p "test_*.py" -v` first ran 662 tests and failed on 15 stale docs-contract assertions after Batch 17 wording displaced Batch 16 exact phrases; after docs compatibility sync the rerun ran 662 tests with `OK` in 671.629s using `timeout_ms: 1200000`. `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` for 91 fixture directories with renderer file count 191. `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 17 sessions and 0 failures. `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Track 10 Task 25 Batch 17 docs/build/diff hygiene: `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_batch17_site` exited `0`; disposable `.mkdocs_task25_batch17_site` was removed; `git diff --check` exited `0`; git staging/commit/push/PR remains explicit-only.
- Track 10 Task 25 future-gated extension matrix docs check: `python -m unittest tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track10_task25_future_gated_extension_matrix_is_staged -v` ran 1 test with `OK`; `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 18 tests with `OK`; `python tools\check_docs.py` passed; `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task25_future_matrix_site` exited `0`; disposable `.mkdocs_task25_future_matrix_site` was removed; `git diff --check` exited `0`.
- Track 10 Task 25 expected focused verification after implementation: `python -m unittest tests.product_agent_os.test_project_code_graph tests.product_agent_os.test_project_graph_manifest tests.product_agent_os.test_project_graph_observations tests.product_agent_os.test_project_graph_ontology tests.product_agent_os.test_project_graph_overlays tests.product_agent_os.test_project_graph_analysis tests.product_agent_os.test_project_graph_queries tests.product_agent_os.test_project_graph_visual_model tests.product_agent_os.test_project_graph_renderer tests.product_agent_os.test_project_cockpit_model tests.product_agent_os.test_project_graph_cli tests.product_agent_os.test_project_graph_safety -v`, adjacent status/runtime/fixture/lifecycle/docs tests, fixture eval, transcript eval, docs check, visual QA checks when implemented and `git diff --check`. Full unittest wrappers must use `timeout_ms: 1200000`.
- Track 10 Task 25 visual-map planning/control-plane sync verification: `python tools\check_docs.py` passed and `git diff --check` exited `0` after replacing the Task 25 matrix with V2 `T10-CG-V2-M01..M32`, updating batches 13-18 and syncing root system-file status. This planning baseline is superseded by the Batch 13 and Batch 14 implementation evidence above.
- Track 10 Task 24 Batch 12 status: `T10-SV-M58..M62` docs/control-plane/final verification closure is implemented for `agent_skill_metrics_loop` docs, source registry, Track 10 backlog, root control-plane evidence and explicit-only git boundary.
- Track 10 Task 24 Batch 12 focused docs RED/GREEN check: `python -m unittest tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track10_task24_self_verification_docs_and_control_plane_are_synced -v` failed before docs sync on missing Product-Agent OS docs, README, source registry, backlog and root control-plane terms, then passed with `OK`.
- Track 10 Task 24 Batch 12 focused docs/source-policy check: `python -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_source_policy -v` ran 23 tests with `OK`.
- Track 10 Task 24 Batch 12 full verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 584 tests with `OK` in 551.714s, then reran after evidence notes and ran 584 tests with `OK` in 504.793s using `timeout_ms: 1200000`; fixture eval exited `0` for 85 fixture directories with `renderer_file_count: 191`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`; commit/push/PR remains explicit-only.
- Track 10 Task 24 Batch 11 status: `T10-SV-M46..M57` is implemented for status snapshot metrics summaries, discovery/applicability gates, methodology audit recommendations, runtime packet validation, review-only route options, guided question routing, lifecycle skill wording, fixture false-positive coverage, behavioral eval cases and transcript sessions.
- Track 10 Task 24 Batch 11 RED evidence: focused Batch 11 suite failed before implementation on missing status/discovery/audit/runtime/lifecycle/eval contracts.
- Track 10 Task 24 Batch 11 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_question_protocol tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_infrastructure_templates -v` ran 306 tests with `OK`.
- Track 10 Task 24 Batch 11 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 583 tests with `OK` in 636.067s using `timeout_ms: 1200000`.
- Track 10 Task 24 Batch 11 fixture/transcript/compatibility/docs checks: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 85 fixtures, 0 failures and `renderer_file_count: 191`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_source_policy -v` ran 22 tests with `OK`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.
- Track 10 Task 24 Batch 10 status: `T10-SV-M29..M45` plus guardrails `T10-SV-G4..G6` are implemented for trace data-classification, shared offline artifact safety, scorecard ledger, daily/weekly packets, component prioritization, modernization candidates, offline report rendering, CLI staging, no-baseline renderer pollution and metrics automation candidate-only blocking.
- Track 10 Task 24 Batch 10 RED evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_agent_skill_metrics_report tests.product_agent_os.test_agent_skill_metrics_cli tests.product_agent_os.test_status_dashboard tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_automation_policy -v` failed before implementation on missing Batch 10 imports/modules/templates and metrics automation blocking.
- Track 10 Task 24 Batch 10 focused GREEN evidence: the same focused suite ran 127 tests with `OK`; `python -m unittest tests.product_agent_os.test_fixture_eval_runner -v` ran 17 tests with `OK` in 297.894s.
- Track 10 Task 24 Batch 10 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 575 tests with `OK` in 612.098s using `timeout_ms: 1200000`.
- Track 10 Task 24 Batch 10 fixture/transcript/compatibility/docs/diff checks: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures and `renderer_file_count: 191`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.
- Track 10 Task 24 Batch 9 status: `T10-SV-M17..M28` is implemented for metric aggregation, repeatability, scorecard, confidence/gate, cadence and run-record contract surfaces in `agent_skill_metrics.py`.
- Track 10 Task 24 Batch 9 RED evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` failed before implementation with `ImportError: cannot import name 'build_metric_aggregation'`.
- Track 10 Task 24 Batch 9 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 17 tests with `OK`.
- Track 10 Task 24 Batch 9 reuse-first adjacent checks: `python -m unittest tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard -v` ran 28 tests with `OK`; `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_automation_policy -v` ran 87 tests with `OK`; `python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_transcript_session_evals -v` ran 21 tests with `OK` using a long wrapper timeout.
- Track 10 Task 24 Batch 9 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 560 tests with `OK` in 809.106s using `timeout_ms: 900000`.
- Track 10 Task 24 Batch 9 fixture/transcript/compatibility/docs/diff checks: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 187`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.
- Track 10 Task 24 Batch 8 status: `T10-SV-M5..M16` is implemented for trace/redaction/dataset/grader/judge contract surfaces in `agent_skill_metrics.py`; later metrics, report/CLI, runtime/lifecycle/eval and docs/full-verification batches remain queued.
- Track 10 Task 24 Batch 8 RED evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` failed before implementation with `ImportError: cannot import name 'build_evidence_dataset'`.
- Track 10 Task 24 Batch 8 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 11 tests with `OK`.
- Track 10 Task 24 Batch 8 reuse-first adjacent checks: `python -m unittest tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard -v` ran 22 tests with `OK`; `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_automation_policy -v` ran 87 tests with `OK`; `python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_transcript_session_evals -v` ran 21 tests with `OK` after rerunning with a 10-minute tool timeout.
- Track 10 Task 24 Batch 8 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 554 tests with `OK` using `timeout_ms: 600000`.
- Track 10 Task 24 Batch 8 fixture/transcript/compatibility/docs/diff checks: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 187`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.
- Track 10 Task 24 Batch 7 status: `T10-SV-M-1..M4` plus guardrails `T10-SV-G1..G3` are implemented for foundation/registry surfaces in `agent_skill_metrics.py`.
- Track 10 Task 24 Batch 7 RED evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` failed before implementation with `ModuleNotFoundError: No module named 'product_agent_os.agent_skill_metrics'`; stale-evidence RED then failed before stale marker support.
- Track 10 Task 24 Batch 7 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_agent_skill_metrics -v` ran 5 tests with `OK`.
- Track 10 Task 24 Batch 7 reuse-first adjacent checks: `python -m unittest tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_status_snapshot tests.product_agent_os.test_status_dashboard -v` ran 16 tests with `OK`; `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_automation_policy -v` ran 87 tests with `OK`.
- Track 10 Task 24 Batch 7 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 548 tests with `OK`.
- Track 10 Task 24 Batch 7 fixture/transcript/compatibility/docs/diff checks: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 187`; transcript eval exited `0` with 10 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.
- Track 10 Task 24 root system-file sync verification: `python tools\check_docs.py` passed and `git diff --check` exited `0` after Task 24 matrix/control-plane sync.
- Track 10 Task 23 Batch 6 full verification: `python -m unittest discover -s tests -p "test_*.py" -v` ran 543 tests with `OK`.
- Track 10 Task 23 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; runner output kept `renderer_file_count: 187` and all emitted fixture records had `ok: true`.
- Track 10 Task 23 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 10 sessions and 0 failures.
- Track 10 Task 23 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Track 10 Task 23 docs/build/diff hygiene: `python tools\check_docs.py` passed, strict MkDocs exited `0` with `PYTHONPATH=C:\tmp\codex_docs_mkdocs` and disposable `--site-dir .mkdocs_task23_site`, the disposable site directory was removed, and `git diff --check` exited `0`.
- Track 10 Task 23 commit boundary: no `git add`, `git commit`, `git push` or PR creation was executed; `T10-Q-M25` remains explicit-approval-only.
- Task 22 final documentation sync closure: focused docs tests `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 13 tests with `OK`.
- Task 22 full verification baseline: `python -m unittest discover -s tests -p "test_*.py" -v` ran 520 tests with `OK`.
- Task 22 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures, 0 failures and renderer file count 186.
- Task 22 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Task 22 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Task 22 docs/build/diff hygiene: `python tools\check_docs.py` passed, strict MkDocs exited `0` with `PYTHONPATH=C:\tmp\codex_docs_mkdocs` and disposable `--site-dir .mkdocs_task22_site`, and `git diff --check` exited `0`.
- T9-D6 RED checks: focused catalog/audit/discovery/template/lifecycle/behavioral/fixture checks failed as expected before implementation on missing `frontend` gates, audit recommendations, discovery signals, five Frontend templates, lifecycle skill routing, behavioral eval coverage and fixture eval check.
- Focused T9-D6 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v` ran 200 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; renderer file count is 107 and `frontend_contract_present` is true.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 386 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.
- T9-D8 status: API & Integrations methodology integration is implemented.
- Latest focused T9-D8 checks: API catalog/audit/discovery/template/lifecycle/docs/fixture suite ran 242 tests with `OK`.
- Latest fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 45 fixtures, 0 failures, renderer file count 128 and `api_integrations_contract_present: true`.
- Latest full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 424 tests with `OK`.
- Latest transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Latest Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- T9-D9 status: Database & Data methodology integration is implemented.
- Latest focused T9-D9 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 234 tests with `OK`.
- Latest T9-D9 fixture runner tests: `python -m unittest tests.product_agent_os.test_fixture_eval_runner -v` ran 15 tests with `OK`.
- Latest fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 49 fixtures, 0 failures, renderer file count 142 and `database_data_contract_present: true`.
- Latest full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 433 tests with `OK`.
- Latest transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Latest Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest docs/build/diff hygiene: `python tools\check_docs.py` passed, strict MkDocs exited `0` with `PYTHONPATH=C:\tmp\codex_docs_mkdocs`, and `git diff --check` exited `0`.
- T9-D10 status: LLM / AI / RAG methodology integration is implemented through `M30..M36`.
- Latest T9-D10 focused AI/RAG fast suite: `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixtures tests.product_agent_os.test_discovery tests.product_agent_os.test_lifecycle_skills -v` ran 190 tests with `OK`.
- Latest T9-D10 focused fixture runner suite: `python -m unittest tests.product_agent_os.test_fixture_eval_runner -v` ran 15 tests with `OK`.
- Latest T9-D10 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 54 fixtures, 0 failures, renderer file count 157 and `llm_ai_rag_contract_present: true`.
- Latest T9-D10 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 445 tests with `OK`.
- Latest T9-D10 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-D10 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-D10 docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- Latest T9-D10 M30..M36 focused contract check: focused handoff/tooling/model/RAG lifecycle/diff/incident/report tests ran 6 tests with `OK`.
- Latest T9-D10 final full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 449 tests with `OK`.
- Latest T9-D10 final fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 54 fixtures, renderer file count 157 and `llm_ai_rag_contract_present: true`.
- Latest T9-D10 final transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-D10 final Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-D10 final docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- T9-D11 status: Security, Privacy & Compliance methodology integration is implemented.
- Latest T9-D11 focused security suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v` ran 81 tests with `OK`.
- Latest T9-D11 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 57 fixtures, 0 failures, renderer file count 173 and `security_privacy_compliance_contract_present: true`.
- Latest T9-D11 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 460 tests with `OK`.
- Latest T9-D11 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-D11 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-D11 docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- T9-D12 status: Delivery, Release & Operations methodology integration is implemented.
- Latest T9-D12 final focused delivery suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_report tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 298 tests with `OK`.
- Latest T9-D12 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 66 fixtures, 0 failures, renderer file count 186 and `delivery_release_operations_contract_present: true`.
- Latest T9-D12 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 478 tests with `OK`.
- Latest T9-D12 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-D12 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-D12 docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- T9-S Task 20 status: Cross-Domain Synthesis is implemented through `M10..M14`.
- Latest T9-S M10..M14 RED checks failed as expected before implementation on missing cross-domain fixture checks, methodology report synthesis rendering, lifecycle skill packet wording, behavioral eval case coverage and docs/backlog sync.
- Latest T9-S M10..M14 focused GREEN check: `python -m unittest tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_cross_domain_synthesis_fixtures tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_expected_renderer_behavior_by_fixture tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_required_fixture_projects_exist tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_false_positive_scenario_fixtures_are_synthetic_and_secret_free tests.product_agent_os.test_methodology_report.MethodologyReportTest.test_report_renders_cross_domain_synthesis_groups_and_source_ledger tests.product_agent_os.test_lifecycle_skills.LifecycleSkillsTest.test_lifecycle_skills_consume_cross_domain_synthesis_packets tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_template_validates_expected_contract tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_cases_encode_forbidden_shortcuts tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track9_cross_domain_synthesis_docs_and_backlog_are_synced -v` ran 9 tests with `OK`.
- Latest T9-S M10..M14 focused synthesis suite: `python -m unittest tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_methodology_report tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 316 tests with `OK`.
- Latest T9-S M10..M14 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 73 fixtures, 0 failures, renderer file count 186 and `cross_domain_synthesis_contract_present: true`.
- Latest T9-S M10..M14 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 496 tests with `OK`.
- Latest T9-S M10..M14 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-S M10..M14 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-S M10..M14 docs/diff hygiene: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 11 tests with `OK`, `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- T9-R Task 21 status: Runtime Runner And Finish Options is implemented through `M25`.
- Latest T9-R M0..M6 focused runtime suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v` ran 28 tests with `OK`.
- Latest T9-R M7..M13 focused runtime suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_codex_runner_fixtures_are_synthetic tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_required_fixture_projects_exist -v` ran 36 tests with `OK`.
- Latest T9-R M7..M13 guard suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_guards -v` ran 6 tests with `OK`.
- Latest T9-R M7..M13 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 508 tests with `OK`.
- Latest T9-R M7..M13 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures, 0 failures, 13 codex-runner fixtures and runtime methodology checks all `true`.
- Latest T9-R M7..M13 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-R M7..M13 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-R M16..M25 focused runtime/template suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_behavioral_workflow_evals -v` ran 109 tests with `OK`.
- Latest T9-R M16..M25 CLI suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli -v` ran 10 tests with `OK`.
- Latest T9-R M16..M25 runtime fixture suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v` ran 6 tests with `OK`.
- Latest T9-R M16..M25 full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 518 tests with `OK`.
- Latest T9-R M16..M25 fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures, 0 failures, renderer file count 186, 16 codex-runner fixtures, `runtime_cross_domain_bridge_present: true` and `runtime_first_response_compact: true`.
- Latest T9-R M16..M25 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Latest T9-R M16..M25 Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Latest T9-R M16..M25 docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- Track 10 Task 23 status: `T10-Q-M15..M22` adds fixture eval, behavioral eval, transcript eval, lifecycle skill and docs/source-registry coverage for Task 23 guided question protocol and status dashboard; `T10-Q-M23..M25` full verification is complete.
- Track 10 Batch 5 contract targets: `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, and `stale_evidence_no_success_claim`.
- Task 23 guided question protocol and status dashboard focused RED evidence: `python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_transcript_session_evals -v` failed before implementation on missing Batch 5 fixture checks, lifecycle wording, docs/source registry sync and transcript cases.
- Task 23 Batch 5 focused GREEN evidence: `python -m unittest tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_transcript_session_evals -v` ran 83 tests with `OK`.
- Task 23 Batch 5 transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 10 sessions and 0 failures.
- Task 23 Batch 5 docs/diff hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0`.
- Track 10 plan hygiene: `python tools\check_docs.py` passed and `git diff --check` exited `0` after creating the plan; Task 24 matrix and root system-file sync require the same docs/diff checks.

## Required Checks After Docs Changes

```powershell
python tools\check_docs.py
```

Run strict MkDocs when navigation, Mermaid diagrams, Markdown extensions or MkDocs config change:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

## Required Checks After Plugin Changes

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

Codex App/tool timeout: run the full unittest command with at least 20 minutes of command wait time (`timeout_ms: 1200000`). The current full suite took 809.106s in Track 10 Task 24 Batch 9 and 636.067s in Batch 11, so exact 10-minute or shorter tool timeouts create false timeouts and duplicate reruns.

## Required Checks For Track 10 Implementation

Before Track 10 `Task 23` or `Task 24` implementation:

- Confirm Track 9 `Task 22` is closed and the legacy Track 9 final verification baseline is recorded in Task 22 evidence.
- Re-read `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- For Batch 5, run focused checks covering fixture eval runner, lifecycle skills, Product-Agent OS docs and transcript/session evals before claiming closure.
- For Task 24 Batch 7, focused RED/GREEN checks cover target registry, evidence intake, source priority, stale/failed/accepted-gap evidence, metrics packet bounds and reuse-first guardrails.
- For Task 24 Batch 8, focused RED/GREEN checks cover trace normalization, metrics redaction gate, dataset split/leakage/quality, local grader summaries and judge calibration blocking.
- For Task 24 Batch 9, focused RED/GREEN checks cover metric aggregation, repeatability, scorecards, confidence gates, cadence recommendations and run-record redaction.
- For Task 24 Batch 10, focused RED/GREEN checks cover scorecard ledger, offline HTML report, CLI staging, automation candidate blocking, trace data-classification, shared offline safety and no-baseline-renderer-pollution.
- For Task 24 Batch 11, focused RED/GREEN checks cover runtime packets, lifecycle wording, fixture eval fields, behavioral/transcript sessions and false-positive guards.
- For later Task 24 batches, run focused checks for docs closure and final control-plane evidence before broad verification.
- Inspect current `discovery.py`, `methodology_audit.py`, `methodology_synthesis.py`, `codex_runtime_runner/contracts.py`, `codex_runtime_runner/routes.py`, `infrastructure.py`, `templates.py`, fixture eval runner, lifecycle skills and docs.
- Inspect and reuse existing `question_protocol.py`, `status_snapshot.py`, `status_dashboard.py`, `automation_policy.py`, `codex_runtime_runner/redaction.py`, `agent-eval-workflow.md`, `skill-promotion-record.md`, `trace-evidence-packet.md`, `eval-run-report.md` and `automation-candidate.md` before adding Task 24 code.

For Track 10 code/template/test changes, run focused tests first, then:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Use the same 20-minute minimum command timeout (`timeout_ms: 1200000`) for the full unittest command here.

## Track 9 Section Verification Protocol

Before implementing a Track 9 section:

- Inspect the relevant task block in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Inspect the matching source file under `docs/methodologies/`.
- If the deep audit changes scope, update the plan or Track 9 backlog first and run `python tools\check_docs.py`.

For each Track 9 implementation section:

- Add focused RED tests for new catalog, discovery, readiness gate, artifact template, lifecycle skill or eval behavior before implementation.
- Add false-positive tests when a methodology can be over-applied.
- Run focused tests for the touched section before the full suite.
- Run full plugin verification after plugin scripts, templates, fixtures or tests change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

Use the same 20-minute minimum command timeout (`timeout_ms: 1200000`) for the full unittest command here.

## Completed Focused Checks For T8-C

- Added RED then GREEN tests for `docs-tooling-decision.md` and `T8-A11` docs-as-code applicability statuses.
- Confirmed `docs_as_code_impact` supports `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Added docs tooling selector tests for stack-appropriate recommendations, including MkDocs, Storybook, OpenAPI, DBML/dbdocs, Mermaid, PlantUML and Structurizr DSL.
- Confirmed docs tooling is not forced on backend, native, simple MVP, docs-light or internal-only work when not applicable.
- Confirmed hosted docs and DB introspection stay `approval_required`, not activated.
- Added readiness/eval/fixture coverage through `project-readiness.json` and `docs_tooling_selector_contract_present`.

## Completed Focused Checks For T8-F

- Added RED then GREEN tests for conditional readiness statuses across remaining methodology/tooling gates.
- Confirmed `project-readiness.json` defines `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Confirmed every conditional readiness gate records `applies_when`, `pass_condition`, `accepted_gap`, `required_evidence`, `owner` and `residual_risk`.
- Confirmed fixture eval exposes `conditional_readiness_gates_contract_present`.
- Confirmed lifecycle guidance says detection alone only supports `present_unverified`, not readiness.

## Completed Focused Checks For T8-H

- Added RED then GREEN docs contract tests for `scenarios.md`, `behavioral-evals.md` and `codex-compatibility.md`.
- Confirmed each page has `Source status:`, Inputs, Outputs, Verification and Risks sections.
- Confirmed MkDocs nav and `tools/check_docs.py` include the new pages.
- Confirmed source registry and Track 8 backlog record T8-H closure.

## Completed Focused Checks For T8-GY

- Added RED then GREEN tests for `evaluate_transcript_sessions`, synthetic session fixture replay, privacy/no-secrets rejection and CLI exit codes.
- Confirmed packaged transcript sessions map to `behavioral_case` entries in `behavioral-workflows.json`.
- Confirmed fixture eval exposes `transcript_session_eval_runner_contract_present`.
- Confirmed unsafe transcript content is reported through `privacy_errors` without echoing raw secret-like text, local user paths or raw private chat log markers.

## Completed Focused Checks For T8-B

- Added RED then GREEN tests for `governance-proposal.md`, standards trigger template coverage, readiness gate coverage, fixture eval coverage and lifecycle skill wording.
- Confirmed ADR trigger policy covers architecture boundary, API contract, storage, auth/security, irreversible migration and automation activation with `not_applicable` or accepted-gap options.
- Confirmed C4/arc42, OpenAPI source of truth vs Swagger UI, AsyncAPI producer/consumer compatibility fields, SemVer impact and Keep a Changelog categories are represented in templates.
- Confirmed CODEOWNERS status and GitHub Actions least-privilege proposals stay staged through `governance-proposal.md` with no forced external activation.
- Confirmed fixture eval exposes `standards_trigger_contract_present`.

## Completed Focused Checks For T8-GX

- Added RED then GREEN tests requiring five false-positive/approval-bound fixtures and fixture eval keys.
- Confirmed `backend-no-fsd` and `native-no-fsd` do not set `fsd_structure`.
- Confirmed `simple-crud-no-ddd` does not force `domain_model_when_complex_domain`.
- Confirmed `docs-light-no-portal` does not select MkDocs, Docusaurus, Sphinx, Antora or Read the Docs.
- Confirmed `hosted-docs-approval` keeps hosted docs and DB introspection as `approval_required`.
- Confirmed new fixtures are synthetic and secret-free.

## Completed Focused Checks For T8-D

- Added RED then GREEN tests for top-level `methodology_applicability` discovery packets.
- Confirmed every packet has `status`, `applies_when`, `reason`, `evidence`, `required_evidence`, `owner` and `residual_risk`.
- Confirmed status transitions for complex-domain DDD (`applicable_missing`), applicable FSD structure (`present_unverified`), docs tooling approval boundaries (`approval_required`) and standards trigger context (`present_unverified`).
- Confirmed fixture eval exposes `methodology_applicability_contract_present`.

## Completed Focused Checks For T9-D1

- Added RED then GREEN tests for `business_product` catalog contract, audit recommendations, staged product templates, lifecycle skill wording and fixture eval coverage.
- Confirmed `business_product_contract_present` covers product hypothesis, value proposition, opportunity framing, decision horizon, metric scope, analytics tracking, qualitative feedback, release measurement and workflow-promotion value evidence.
- Confirmed typo-only docs edits, formatting-only edits and dependency pins without behavior impact keep Business/Product methodology not applicable.

## Completed Focused Checks For T9-D2

- Added RED then GREEN tests for `requirements_domain` catalog contract, audit recommendations, staged requirements/domain templates, lifecycle skill wording and fixture eval coverage.
- Confirmed behavior-changing work without acceptance scenarios is a `P0_blocker`.
- Confirmed risky/public-contract work requires requirement quality, stable IDs, constraints traceability and API/UI/data traceability.
- Confirmed unclear stories, business rules, domain events, owner review, accepted gaps, declarative scenario quality and requirement change impact produce deterministic recommendations.
- Confirmed unsupported methodology claims are rejected as evidence: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language and OpenAPI is requirements source of truth.

## Completed Focused Checks For T9-D3

- Added RED then GREEN tests for `solution_architecture` catalog contract, audit recommendations, staged architecture templates, lifecycle skill wording and fixture eval coverage.
- Confirmed multi-surface public API/data/runtime work produces architecture recommendations for scope, context/container boundaries, boundary owner, public contract trace, data ownership, trust boundary review, ADR, observability, rollback, diagram render checks and fitness functions.
- Confirmed typo-only docs edits, formatting-only edits, docs-light prototypes without reviewed/diffable diagrams and non-cloud work without Well-Architected review keep Solution Architecture methodology not applicable.
- Confirmed unsupported architecture claims are rejected as evidence: architecture means diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves architecture quality, architecture-as-code is always required and AI can design architecture from chat alone.
- Confirmed fixture eval exposes `solution_architecture_contract_present`.

## Completed Focused Checks For T9-D4

- Added RED then GREEN tests for `quality_testing_evals` catalog contract, audit recommendations, discovery signals, staged quality templates, lifecycle skill wording, behavioral eval coverage and fixture eval coverage.
- Confirmed missing local command/evidence and completion claims without current evidence are `P0_blocker`.
- Confirmed risky scope, acceptance traceability, deterministic change, API/event/schema contracts, runtime/manual/visual evidence, AI eval reruns, CI gates, test data privacy, bug reproduction and regression impact produce deterministic recommendations with stable artifacts.
- Confirmed typo-only docs edits, formatting-only edits, docs-only source cleanup and dependency metadata without behavior impact keep Quality, Testing & Evals methodology not applicable.
- Confirmed unsupported quality claims are rejected as evidence: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Confirmed fixture eval exposes `quality_testing_evals_contract_present`.

## Completed Focused Checks For T9-D5

- Added RED then GREEN tests for `codex_agentic_workflow` catalog contract, audit recommendations, discovery signals, staged Codex workflow templates, lifecycle skill wording, behavioral eval coverage and fixture eval coverage.
- Confirmed missing control plane, missing source of truth, side-effecting MCP without permission review, hook activation without approval, overlapping subagent work, automation without manual stability and completion claims without evidence produce deterministic recommendations.
- Confirmed simple docs/local work does not force subagents, worktrees, MCP review, hooks, plugin packaging, automation, Agents SDK orchestration or agent evals.
- Confirmed unsupported agentic workflow claims are rejected as evidence: memory as source of truth, subagents always faster, MCP safe by default, hooks harmless, immediate automation, Agents SDK equals Codex runtime and inspection proves completion.
- Confirmed fixture eval exposes `codex_agentic_workflow_contract_present`.

## Completed Focused Checks For T9-D6

- Added RED then GREEN tests for `frontend` catalog contract, audit recommendations, discovery signals, staged frontend templates, lifecycle skill wording, behavioral eval coverage, synthetic frontend fixture and fixture eval coverage.
- Confirmed user-visible UI work routes to Frontend methodology with `present_unverified` discovery status until current evidence exists.
- Confirmed backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD work does not force frontend gates.
- Confirmed Storybook and Feature-Sliced Design are conditional, not proof by themselves.
- Confirmed unsupported frontend claims are rejected as evidence: FSD mandatory, Storybook proves UI quality, automated a11y addon enough, desktop screenshot proves responsive UI, lab Web Vitals always represent production UX and code inspection proves UI completion.
- Confirmed fixture eval exposes `frontend_contract_present`.

## Completed Focused Checks For T9-D7 Through M29

- Added RED then GREEN tests for backend resilience/operations depth in artifact templates, audit recommendations and fixture eval contract terms.
- Confirmed backend dependency failure matrix requires per dependency timeout, retry/backoff/max attempts, circuit breaker non-applicability, fallback, alert owner and verification evidence.

## Completed Focused Checks For T9-D7 Through M39

- Added RED then GREEN tests for backend requirements intake, security-note depth, observability semantics, health verification policy, operational runbook depth, config/secrets privacy constraints, rollback release depth, contract-aware backend evidence and backend dependency categories.
- Confirmed discovery exposes `backend_dependency_signals` for database, message broker, cache, payment, email, storage, search and third-party HTTP/provider clients, with `present_unverified` status until owner review and runtime/contract evidence exist.
- Confirmed `requirements-author`, generated `REQUIREMENTS.md`, backend templates, `methodology_audit.py`, `run_fixture_eval.py` and the synthetic `backend-service-app` fixture include the new batch terms.
- Confirmed job/queue policy records payload contract, retry policy, dead-letter behavior, dead-letter queue, idempotency key, replay procedure, poison-message handling, deduplication, ordering and backpressure.
- Confirmed data consistency policy records local transaction, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path.
- Confirmed observability rejects logs-only evidence and requires traces, metrics, logs, dashboards, alerts, correlation IDs, alert ownership, redaction and no-private-payload logging.
- Confirmed SLI/SLO or explicit gap, health endpoint semantics, operational owner/escalation handoff, rollback command/manual procedure, data recovery/replay, irreversible side effects, owner approval and residual risk are represented.
- Confirmed Twelve-Factor vocabulary stays optional and framework-agnostic while recording explicit dependencies, build-release-run, process model, admin tasks, dev/prod parity, logs-as-event-stream and stateless process or accepted gap.
- Confirmed service boundary changes require owner review, decision authority, boundary rationale and ADR link or accepted gap.

## Completed Focused Checks For T9-D7 Through M45

- Added RED then GREEN tests for backend delivery discovery signals, retry/idempotency lightweight detection, severity policy, stack-specific snippet deferral, Product-Agent OS docs/source sync and semantic evidence sufficiency routing.
- Confirmed discovery exposes `backend_delivery_signals` for backend stack, commands, CI, APIs, DB, queues, workers, deployment manifests and security signals without executing deployments or external writes.
- Confirmed discovery exposes `backend_resilience_signals` as lightweight read-only retry/idempotency, dependency context and job context signals, with deeper static analysis deferred to avoid false positives.
- Confirmed risky production backend keeps service boundary/runtime blockers and high-risk security/rollback/observability/SLO/health gaps, while complete accepted-gap fields downgrade eligible high-risk recommendations and simple local/backend-light work stays warning-level.
- Confirmed T9-D7 templates stay framework-agnostic and defer Node.js, Python, Java, .NET and Go snippets until stack-specific owner/examples/verification exist.
- Confirmed generated `EVALS.md`, `RUNLOG.md` and audit recommendations route owner reviewed test/eval/runtime evidence sufficiency to T9-S/cross-domain semantic sufficiency backlog.

## Completed Focused Checks For T9-D8

- Added RED then GREEN tests for `api_integrations` catalog, audit, discovery, readiness/control-plane templates, lifecycle skills, docs/source sync, fixture eval coverage and false-positive fixtures.
- Confirmed discovery exposes API contract source signals for OpenAPI, Swagger source files, AsyncAPI, GraphQL, protobuf, JSON Schema, Pact, webhooks/events, generated clients and external providers.
- Confirmed Swagger UI/rendered docs are not treated as source of truth, schema validation alone is not contract testing, OAuth alone is not complete security evidence and GraphQL/gRPC/events are not universal defaults.
- Confirmed API-only contract fixtures do not force Backend blockers, while external writes stay `approval_required`.
- Confirmed staged artifacts cover API inventory, consumer map, compatibility, errors, auth/authorization, contract tests, generated SDKs, webhooks, external approvals and API style decisions.
- Confirmed fixture eval exposes `api_integrations_contract_present` with 45 fixtures, 0 failures and renderer file count 128.

## Completed Focused Checks For T9-D9

- Added RED then GREEN tests for `database_data` catalog, audit, discovery, readiness/control-plane templates, lifecycle skills, docs/source sync, fixture eval coverage and false-positive fixtures.
- Confirmed discovery exposes `database_data_signals` while preserving backward-compatible `data_migration_signals`.
- Confirmed schema-only artifacts are `present_unverified`, not safety proof, and do not automatically claim migration/runtime readiness.
- Confirmed production DB/data access, migration execution, backup restore, retention mutation and destructive migration stay `approval_required`.
- Confirmed stack-specific database tooling has no universal default; schema-diff tooling deferred until owner, safety policy and verification evidence exist.
- Confirmed staged artifacts cover inventory, dictionary, migration plan, expand-contract, backfill, rollback feasibility, backup/restore, classification, data quality, data contract, lineage, query performance, retention/deletion, synthetic fixtures and production access approval.
- Confirmed fixture eval exposes `database_data_contract_present` with 49 fixtures, 0 failures and renderer file count 142.

## Completed Focused Checks For T9-D10 Through M29

- Added RED then GREEN tests for AI/RAG template alias compatibility, renderer target registration, strengthened AI eval workflow/spec terms, generated control-plane evidence fields, behavioral/transcript coverage, synthetic AI/RAG fixtures, fixture eval contract coverage and lifecycle skill routing.
- Confirmed source-aligned template names are canonical: `prompt-contract.md`, `model-decision-record.md` and `rag-eval-report.md`; legacy plan names are mapped through `AI_RAG_TEMPLATE_ALIASES` without duplicate generated contracts.
- Confirmed the renderer now stages 15 AI/RAG artifact templates under `.codex/artifact-templates/` and raises the `python-app` renderer file count from 142 to 157.
- Confirmed `ai-eval-regression.md` and `ai-eval-spec.md` require app-backed eval path, baseline/current comparison, prompt/context inventory, retrieval metrics, grounding evidence, dataset governance, thresholds, failed cases and current-run evidence before AI quality claims.
- Confirmed `llm-ai-rag-evidence-before-completion` behavioral eval coverage and a fifth transcript session reject prompt-inspection-only and current-evidence-free AI/RAG quality claims.
- Confirmed synthetic AI/RAG fixtures cover prompt/model change, tool approval boundary, structured output, agent trace, latency/cost budget and RAG quality regression without secrets, tokens, raw private chats, customer data or live API keys.
- Confirmed lifecycle skills route `llm_ai_rag` methodology without forcing one eval runner, multi-agent architecture or live model/API calls.

## Completed Focused Checks For T9-D10 Through M36

- Added RED then GREEN tests for agent handoff compatibility, eval tooling selector/deferred runner policy, model migration thresholds, RAG deletion/privacy lifecycle, AI behavior diff-signal policy, AI incident workflow and methodology report rendering.
- Confirmed `agent-handoff-contract.md` is mapped to existing `agent-task-packet.md` without registering a duplicate generated contract.
- Confirmed `ai-eval-spec.md` records Promptfoo, OpenAI Evals, pytest/Jest, Ragas, LangSmith, selected/rejected runner rationale, deferred decision and no forced eval runner.
- Confirmed `model-decision-record.md`, `eval-run-report.md`, RAG source/retrieval/dataset templates, `guardrail-matrix.md` and generated `RUNLOG.md` include model migration, threshold, deletion/privacy, incident and Security/Privacy handoff fields.
- Confirmed discovery exposes `diff_signal_policy` as limited to workspace and intent signals, with no external branches, no network and no filename-only certainty.
- Confirmed methodology reports render AI/RAG evidence, approvals, accepted gaps, residual risk and safe next action while redacting local paths, private chat logs and private customer data.

## Completed Focused Checks For T9-D11

- Added RED then GREEN tests for `security_privacy_compliance` catalog, audit recommendations, discovery depth, source-policy redaction, renderer templates, readiness/behavioral evals, lifecycle skill routing, fixture eval coverage and methodology report redaction.
- Confirmed the renderer stages 16 new Security, Privacy & Compliance artifact templates under `.codex/artifact-templates/` and raises the `python-app` renderer file count from 157 to 173.
- Confirmed canonical template names and aliases cover threat surface/model, ASVS/SSDF mapping, secrets inventory/policy, authorization negative tests, audit logging and compliance overlay/applicability without duplicate generated contracts.
- Confirmed source-policy checks block secret-like literals plus raw PII/private data/payment data markers in docs/templates/fixtures.
- Confirmed synthetic security fixtures cover payment/billing high risk, docs-only security article false positive, unsupported compliance claims, CI permissions, SBOM/provenance and no raw secrets/private data.
- Confirmed unsupported security claims are rejected: security review after coding, no-secrets-in-code means safe, ASVS/OWASP proves compliance, SBOM once is enough, Codex Security scan is implied, OAuth proves API security and privacy compliance is universal.

## Completed Focused Checks For T9-D12

- Added RED then GREEN tests for `delivery_release_operations` catalog fields, discovery signals, audit recommendations, template/eval terms, lifecycle skill routing, fixture eval coverage and Product-Agent OS docs sync.
- Confirmed delivery release gates cover release scope, version impact, changelog/release notes, artifact manifest, release evidence before completion, rollout, rollback/recovery, environment approval, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review and automation manual stability.
- Confirmed final release depth covers release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency.
- Confirmed release/publish/deploy/package registry, marketplace/store, CI/CD environment mutation and active automation remain `approval_required` and are not performed by the methodology route.
- Confirmed false-positive fixtures reject docs-only release notes, CI-only workflows, deployment manifests without execution, feature flags without owners, GitOps without approval path, mobile signing alone, DORA individual quota and tooling files without owner evidence.
- Confirmed fixture eval exposes `delivery_release_operations_contract_present` with 66 fixtures, 0 failures and renderer file count 186.

## Completed Focused Checks For T9-S Task 20

- Added RED then GREEN tests for source artifact grouping, source artifact aliases/decisions, owner-question dedupe, risk-aware safe next action, audit/discovery synthesis packets, semantic evidence sufficiency and cross-domain false-positive routing.
- Confirmed `methodology_synthesis` produces grouped recommendations with owner domain, consumer domains, source domains, merged gates, evidence required, approval boundary, accepted-gap option, residual risk and safe next action.
- Confirmed methodology reports render a Cross-Domain Synthesis section and source artifact ledger while preserving redaction and external-action boundary text.
- Confirmed lifecycle skills consume synthesized packets without dumping every methodology gate, scaffolding before approval or treating detection as verification.
- Confirmed packaged mixed-risk fixtures cover small PII app, complex non-production monorepo, internal CLI, AI/RAG plus data/security overlap, package release with security handoff, source artifact alias/deferred mapping and owner-question dedupe.
- Confirmed fixture eval exposes `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present` with 73 fixtures, 0 failures and renderer file count 186.

## Completed Focused Checks For T9-R Task 21 Through M14

- Added RED then GREEN tests for compact runtime methodology packets, route propagation, validation limits, finish options, recommendation-only no-write behavior and detection-only completion blocking.
- Confirmed runtime routes carry `methodology_packet`, `finish_options` and `safe_next_action` without changing runner schema version or introducing model/network/standalone runtime behavior.
- Confirmed high-risk methodology recommendations for publish/deploy/tag/release/PR/push/package registry/marketplace/security scan/production data/DB migration/external mutation are approval-bound and do not perform external action.
- Confirmed automation promotion routes are blocked without manual stability and value/maturity evidence.
- Confirmed methodology route payloads are redacted and malformed packets fail with stable errors rather than tracebacks.
- Confirmed fixture eval exposes `runtime_methodology_packet_present`, `runtime_finish_options_approval_bound`, `runtime_detection_not_completion`, `runtime_external_write_blocked`, `runtime_automation_maturity_required`, `runtime_methodology_redaction_enforced` and `runtime_malformed_methodology_packet_blocked` with 80 fixtures, 0 failures and 13 codex-runner fixtures.
- Confirmed M14 sync records current evidence, residual risks and remaining Task 21 expansion rows before final Track 9 documentation closure.

## Completed Focused Checks For T9-R Task 21 Through M25

- Added RED then GREEN tests for CLI/validator JSON output, generated control-plane/eval/handoff packet support, schema-v1 backward compatibility, lifecycle-status finish-option mapping, cross-domain runtime bridge checks, compact first-response fields, structured high-risk action taxonomy and ownership/parallelism routing.
- Confirmed valid old schema-v1 runner results without `methodology_packet` still validate, while malformed additive `finish_options` fail with stable errors.
- Confirmed CLI output and `--output` JSON carry redacted `methodology_packet`, `finish_options` and compact `first_response_contract` fields; high-risk methodology actions correctly return `needs_approval` while the validator still accepts the JSON shape.
- Confirmed lifecycle statuses map to bounded finish options, and `blocked`/`needs_context` do not offer write or stage actions.
- Confirmed generated `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json`, `behavioral-workflows.json` and `agent-task-packet.md` carry runtime methodology packet fields without dumping every gate or raw conversation history.
- Confirmed fixture eval exposes `runtime_cross_domain_bridge_present` and `runtime_first_response_compact`; runtime bridge checks preserve cross-domain synthesis through routing.
- Confirmed multiple owner domains or overlapping ownership reroute parallel builder work through `agent-team-designer` with fresh-context handoff before subagent work.

## Task 22 final documentation sync closure

- Added RED docs contract coverage with `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`; the RED run failed on missing Task 22 docs, README, source registry and control-plane closure terms before docs edits.
- Required Task 22 verification commands:
  - `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
  - `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`
  - `python tools\check_docs.py`
  - `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict`
  - `python -m unittest discover -s tests -p "test_*.py" -v`
  - `python plugins\product-agent-os\scripts\run_fixture_eval.py`
  - `git diff --check`
- Focused docs tests cover Product-Agent OS full-stack docs, Track 1-9 architecture, Codex-only runtime boundary, methodology packet behavior, readiness vocabulary, scenario finish options, eval limitations, source registry closure and root control-plane closure.
- Final Task 22 verification results:
  - `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 13 tests with `OK`.
  - `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
  - `python tools\check_docs.py` passed.
  - `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict --site-dir .mkdocs_task22_site` exited `0`.
  - `python -m unittest discover -s tests -p "test_*.py" -v` ran 520 tests with `OK`.
  - `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures, 0 failures and renderer file count 186.
  - `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
  - `git diff --check` exited `0`.

## Evidence Format

- Command:
- Exit code:
- Relevant output:
- Files or artifacts inspected:
- Claims still `present_unverified`:
- Residual risk:
<!-- product-agent-os:end test-plan -->
