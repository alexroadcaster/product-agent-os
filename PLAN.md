# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`PLAN.md` is the compact sequencing and rollback layer for current Product-Agent OS work. It points to source-owned plans/backlogs for detailed history and keeps active execution boundaries visible.

## Current Planning Contract

- Work in focused slices with explicit scope, acceptance criteria, risks, rollback and verification gates.
- Use Product-Agent OS skills for requirements, implementation planning, test/eval design, docs maintenance, risk review and completion-skeptic loops when the task matches them.
- Keep historical batch matrices in source-owned files, not in this root plan.
- Do not create/switch branches, stage, commit, push, open PRs, mutate target workspaces, run browser automation, call providers/live APIs, publish, deploy or create automations without exact approval for that action.
- For Product-Agent OS pilots, prefer real-project target evidence where it improves confidence. Keep `codex_docs` as the control-plane, runner and evidence workspace; keep target projects read-only unless a test row names an approved mutation surface, rollback and owner.
- Preserve unrelated dirty work and record only the evidence needed for current handoff.

## Current State

| Workstream | State | Planning impact |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned and closed for completed historical slices. | Use backlogs and registry for historical detail. |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no branch, stage, commit, push or PR. | Future git-write work needs fresh preflight and exact approval. |
| Batch 38 package-source/readiness | Implemented/recorded. `B38-S2` current cache evidence is `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat prior blockers as historical evidence, not current active blockers unless the same condition recurs. |
| `B38-PILOT-NF01` | Docs-only target addendum completed; target apply blocked by `source_policy_status: blocked` and missing target control-plane/source registry artifacts. | Do not mutate target project until source policy and artifacts are resolved. |
| Batch 39 | Executed through `prod_test.md`; `B39-S1` foundational local contracts, `B39-S2` archetype/first-run/three-target evidence, `B39-S3` functional regression/repeatability, `B39-S4` hardening and `B39-S5` closure/go-no-go are recorded through `B39-S5-CLOSURE-A01`. `B39-S5` consumes S4 blockers into a `release=no_go`, `owner_feedback_testing=conditional_go`, `runtime_browser_pilot=approval_required` decision. | Start owner-feedback testing manually from the S5 test plan. No release/readiness claim until owner feedback and any approval-gated runtime/browser evidence exist. |
| Batch 39 real-project targets | Owner clarified that future Product-Agent OS testing should run on real projects, not only internal `codex_docs` fixtures. `SOL 0.6` is the current `B39-TEST-M20` candidate context as a local-first web-desktop target, but it must not be modified. | Use real targets for read-only discovery and evidence first; record target labels, relative paths, counts, digests and approval boundaries in `codex_docs`. Runtime/browser/provider/git/external actions need separate exact approval. |
| Batch 40 completion-skeptic | Local manual foundation closed; automation status `manual_only` and `not_promoted`. | Keep automation promotion candidate-only until gates are satisfied. |
| Batch 41 first-run orchestration | `B41-S1-M01..M05` command/UX contract, `B41-S2-M06..M09` help-only script matrix, `B41-S3-M10..M16` project-analysis summaries, `B41-S4-M17..M20` HTML artifact integration, `B41-S5-M21..M23` guided question UX and `B41-S6-M24..M30` closure evidence are recorded as local/read-only/staged behavior. Owner review of the Neural_Flow artifact exposed a product UX failure: the current HTML is structurally valid but reads as raw white-page diagnostic output. `B41-S7-M31..M39` now implements the corrective cockpit foundation, graph rendering and local UX/safety hardening: `first_run_cockpit_artifact_v1`, primary single-file `index.html` shell, bounded view-model adapter, Graphology-compatible file/source graph, Cosmos.gl static adapter payload, selected-file panel, table fallback, code-graph `not_available` state, graph-summary hotspots, static search/filter controls, progressive diagnostics, static visual QA and offline/privacy/accessibility contracts. Owner selected `Cosmos.gl` as the graph visualization library for the cockpit canvas. | Treat S6 closure as no-go for release/readiness and continue with `B41-S7-M40` before any stronger real-target artifact usefulness claim. M40 has owner approval recorded for Neural_Flow acceptance, browser visual proof, runtime interaction, WCAG-oriented static/browser checks, Cosmos.gl runtime/WebGL checks where local assets/tooling are available, and necessary `codex_docs` cockpit fixes. Release/git/provider/external writes and target source mutation remain out of scope without separate approval. |
| Agent lifecycle and control-plane sync | Current project agents and Product-Agent OS templates route Task Brief / Completion Brief and control-plane sync through `.codex/config.toml` `[product_agent_os.lifecycle_contract]` plus `[workflows]`. | Future Product-Agent OS tasks must load the config-routed workflow, show the visible briefs, then update owned control-plane files or record `not_applicable` / `handoff_required`; no hook or automation was activated. |

## Next Implementation Queue

| Slice | Scope | Owner action | Codex action | Verification |
| --- | --- | --- | --- | --- |
| `B39-S1` | Foundational local evidence package closed for `B39-TEST-M01..M10`. | Review only if S1 evidence needs rework. | Preserve S1 artifacts as source evidence; do not promote to readiness by themselves. | `prod_test.md` attempt rows, focused tests and synthetic artifacts exist; no target mutation occurred. |
| `B39-S2` | First approved Batch 39 subset is recorded through `B39-TEST-M21-A01..A03` with accepted gaps for generated-view-only, read-only real-target evidence and unsupported release/readiness claims. | Review accepted gaps if they affect product confidence; approve any escalation beyond read-only target discovery. | Preserve S2 evidence in `codex_docs`; do not modify `SOL 0.6`, `Neural Flow` or any target without exact approval. | Deterministic commands and manual evidence recorded in `prod_test.md`; target mutation proof and redaction/no-raw-source rules apply. |
| `B39-S3` | Functional regression and repeatability is closed through `B39-TEST-M23..M33`. M23/M24/M28 added new fixes; M25-M27/M29-M32 focused subsystem suites passed; M33 full verification passed. | Review S3 residual risks and approve any escalation beyond local code/tests or read-only target discovery. | Preserve S3 evidence and do not convert it into release/readiness proof. | `docs/superpowers/specs/batch39-s3-functional-regression-summary.json`; full unittest discover 949 OK / 1 skipped; fixture eval 91/91; transcript eval 26/26; Codex compatibility compatible; docs/check/diff OK. |
| `B39-S4` | Production/mass-user hardening has been executed through current local/read-only/contract gates with explicit expected blockers. The remaining blockers are not hidden: MkDocs is unavailable for fresh public site acceptance, runtime/browser proof needs exact disposable target approval, MCP/Context7 live calls need approval, and release/distribution is held for B39-S5. | Review expected blockers and decide which approval-gated real pilot to run after B39-S5. | Preserve S4 evidence; do not claim release readiness, runtime/browser behavior or promotion. | `docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json`; `docs/superpowers/specs/batch39-s4-full-hardening-comparison.json`; `docs/superpowers/specs/batch39-s4-remaining-gates-summary.json`; `docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json`; plus graph-depth and M37-M39 artifacts. |
| `B39-S5` | Closure and next-route decision is recorded as `closed_for_owner_feedback_testing_not_release_ready`. | Review the S5 owner-feedback scenarios and decide which manual test to run first. | Preserve S5 artifacts and keep release/runtime/browser/provider/external actions approval-gated. | `docs/superpowers/specs/batch39-s5-closure-summary.json`; `batch39-s5-go-no-go-decision-packet.json`; `batch39-s5-no-unapproved-actions-proof.json`; `batch39-s5-owner-feedback-test-plan.json`; focused S5 tests. |
| `B41-S1` | First-run command/UX contract implemented for `B41-S1-M01..M05`. | Review B41-S1 behavior only if CLI wording or write boundary should change. | Preserve implemented source evidence; do not claim full B41, real-target pilot, runtime/browser proof or plugin-cache readiness. | `docs/superpowers/specs/batch41-s1-command-contract-summary.json`; focused B41/first-run tests; docs contract tests. |
| `B41-S2` | Help-only all-script registry and safe command matrix implemented for `B41-S2-M06..M09`. | Review approval-gated classification if any skipped script should later get a narrower read-only mode. | Preserve `partial_with_skips` evidence and continue with S3 integrations. | `docs/superpowers/specs/batch41-s2-script-matrix-summary.json`; focused B41 tests. |
| `B41-S3` | Bounded project-analysis summaries implemented for `B41-S3-M10..M16`. | Review whether the first-run packet answers the expected product questions before HTML integration. | Preserve source-policy blocks, graph orientation-only status, static dependency boundary and runtime/browser `approval_required` status. | `docs/superpowers/specs/batch41-s3-project-analysis-summary.json`; focused B41 tests. |
| `B41-S4` | HTML artifact integration implemented for `B41-S4-M17..M20`. | Review generated artifact usefulness and decide whether guided question UX should ask first or render first in ambiguous projects. | Preserve generated-view-only status, baseline comparison visibility and cleanup preview-only boundary; continue with S5. | `docs/superpowers/specs/batch41-s4-html-artifact-summary.json`; focused B41 and first-run renderer tests. |
| `B41-S5` | Guided question UX and answer-ledger routing implemented for `B41-S5-M21..M23`. | Review whether the first response and route options are useful before real-target pilots. | Preserve one-blocking-question maximum, staged-only answer ledger and generated-view-only status; continue with S6. | `docs/superpowers/specs/batch41-s5-guided-questions-summary.json`; focused B41 tests. |
| `B41-S6` | First-run QA/closure evidence recorded for `B41-S6-M24..M30`: M24 synthetic E2E passed, M25 Neural_Flow read-only expected block passed, M26 app-like pilot timed out before clean static evidence, M27 scorecard is owner-feedback pending, M28 verification sweep packet exists, M29 installed plugin cache readiness is approval-required, and M30 records no-go closure. | Review S6 artifacts and choose the next approval-gated route: owner feedback, disposable runtime/browser pilot, plugin cache refresh, or narrower app-like target retest. | Do not claim release readiness, runtime/browser behavior, provider/API quality, target apply safety or installed-plugin readiness from S6 evidence. | `docs/superpowers/specs/batch41-s6-closure-summary.json`; `docs/superpowers/specs/batch41-s6-real-target-pilots-summary.json`; `docs/superpowers/specs/batch41-s6-plugin-cache-readiness.json`; focused S6 tests and final verification sweep. |
| `B41-S7` | `B41-S7-M31..M39` implemented the cockpit foundation, graph rendering, static UX controls, progressive diagnostics, static visual QA and offline/privacy/accessibility hardening after owner review of the Neural_Flow white-page output. `Cosmos.gl` remains the selected graph visualization library, but runtime WebGL execution is not yet claimed. | Continue with `B41-S7-M40` using the owner approval packet: Neural_Flow acceptance, browser visual proof, runtime interaction, WCAG-oriented checks and Cosmos.gl/WebGL checks are approved for execution where tooling/assets permit. | Convert first-run HTML from diagnostic multi-page output into one primary offline cockpit artifact with navigation, project/source graph, code graph where available, Cosmos.gl rendering boundary, progressive disclosure and visual QA. | `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`; `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`; `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`; `docs/superpowers/specs/batch41-s7-m40-owner-approval-packet.json`; `docs/superpowers/specs/batch41-s7-html-cockpit-analysis.txt`; `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; focused B41/first-run tests and future Neural_Flow acceptance pilot evidence. |

## Batch 39 Execution Rules

- `prod_test.md` is the required attempt/failure/fix/retest ledger for Batch 39.
- Each task must record:
  - test id and slice;
  - objective and product value;
  - technical action;
  - owner action vs Codex action;
  - prerequisites and approvals;
  - evidence path or command;
  - result, failure, fix and retest status;
  - residual risk or accepted gap.
- Choosing a project is not automatically required for every preparatory task. It becomes required when a test step needs real target discovery, target-specific evidence, runtime behavior or mutation.
- When a real project is chosen, the default mode is `read_only_target_discovery`: inspect structure, source-policy state, route signals and evidence shape only. Any live server, browser, provider/API, database, git, release, external write or target mutation action must be approved as a separate surface.

## Source Planning Artifacts

| Artifact | Role |
| --- | --- |
| `REQUIREMENTS.md` | Current scope, acceptance and constraints. |
| `TEST.md` | Current verification commands and escalation rules. |
| `EVALS.md` | Current eval rubrics, thresholds and subjective gates. |
| `RUNLOG.md` | Current-cycle handoff and residual risks. |
| `AGENTS.md` | Durable operating rules and current operating status. |
| `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Track 9 implementation plan. |
| `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md` | Track 10 staged plan and status-dashboard history. |
| `docs/sources/product-agent-os-track-8-detailed-backlog.md` | Track 8 detailed scenario/methodology history. |
| `docs/sources/product-agent-os-track-9-backlog.md` | Source-owned Track 9 methodology and verification history. |
| `docs/sources/product-agent-os-track-10-backlog.md` | Source-owned Track 10, Batch 35, Batch 38, Batch 39 and Batch 40 history. |
| `docs/sources/registry.md` and `docs/sources/registry.en.md` | Claim/source registry. |
| `docs/sources/product-agent-os-batch35-approval-packet-draft.md` | Batch 35 approval and execution packet. |
| `prod_test.md` | Batch 39 production test ledger. |
| `.codex/workflows/control-plane-sync.md` | Mandatory before-completion control-plane sync checklist for non-mechanical Product-Agent OS tasks. |

Evidence ownership stays source-routed; `git diff --check` remains part of docs/control-plane verification.

## Compatibility Marker Bank

These lines are compact anchors for existing tests and source-owned history. They are not execution evidence by themselves.

- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- `B38-DOC-M01..M10` implemented.
- `B38-DOC-M04` | P1 | Add end-user first-run walkthrough.
- `B38-DOC-M05` | P1 | Add artifact/output gallery for user-facing value.
- `B38-DOC-M06` | P1 | Define public vs internal documentation IA boundary for `site/`.
- `B38-DOC-M07` | P1 | Compact README sync after source docs are corrected.
- `B38-DOC-M08` | P2 | Keep RU/EN parity for every changed user-facing page.
- `B38-DOC-M09` | P2 | Update source registry and control-plane pointers only where source-backed claims change.
- `B38-DOC-M10` | P2 | Final docs verification and generated `site/` refresh decision.
- B38-S1 `B38-PROD-M01..M03`; M01 `owner_closed_no_op_git_release_pr`; M02 `implemented`; M03 `accepted_gap`.
- B38-S2 `B38-PROD-M04..M05`; M04 `implemented`; M05 `implemented`; blocked_sandbox_cache_write_denied_after_backup_stage; plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage; Next release/install/cache action: no remaining M05 cache refresh action is required.
- B38-S3 `B38-PROD-M06..M09`; M06 `implemented`; M07 `implemented`; M08 `implemented`; M09 `implemented`; no_real_project_execution_performed.
- B38-S4 `B38-PROD-M10..M11`; M10 `reviewed_gap_recorded`; M11 `implemented`; source_policy_status ok; system_file_hygiene_status blocked; fixture_dependency_boundary synthetic_non_install_fixtures_unpinned_dependencies.
- B38-PILOT-NF01 `Neural_Flow`, source_policy_status blocked.
- T10-LIVE-M41 post-B38 audit, historical_preflight_snapshot, future git write, fresh preflight is required before any git write, B37/B38/B38-S1 did not themselves close M41.

| Task | Priority | Summary | Status |
| --- | --- | --- | --- |
| `B38-DOC-M04` | P1 | Add end-user first-run walkthrough. | `implemented` |
| `B38-DOC-M05` | P1 | Add artifact/output gallery for user-facing value. | `implemented` |
| `B38-DOC-M06` | P1 | Define public vs internal documentation IA boundary for `site/`. | `implemented` |
| `B38-DOC-M07` | P1 | Compact README sync after source docs are corrected. | `implemented` |
| `B38-DOC-M08` | P2 | Keep RU/EN parity for every changed user-facing page. | `implemented` |
| `B38-DOC-M09` | P2 | Update source registry and control-plane pointers only where source-backed claims change. | `implemented` |
| `B38-DOC-M10` | P2 | Final docs verification and generated `site/` refresh decision. | `implemented` |
| `B38-PROD-M01` | P0 | Resolve or explicitly defer `T10-LIVE-M41` git release/PR gate. | `owner_closed_no_op` |
| `B38-PROD-M02` | P0 | Freeze install source and package surface. | `implemented` |
| `B38-PROD-M03` | P0 | Finalize public and organization-facing plugin metadata. | `accepted_gap` |
| `B38-PROD-M04` | P0 | Run full pre-install verification. | `implemented` |
| `B38-PROD-M05` | P0 | Refresh or install the new plugin version and prove no stale plugin cache is used. | `implemented` |
| `B38-PROD-M06` | P1 | Create first-run operator packet for real users. | `implemented` |
| `B38-PROD-M07` | P1 | Build real-project pilot target and consent matrix. | `implemented` |
| `B38-PROD-M08` | P1 | Define pilot success criteria and product metrics. | `implemented` |
| `B38-PROD-M09` | P1 | Prepare pilot harness and evidence ledger. | `implemented` |
| `B38-PROD-M10` | P1 | Reconfirm security, privacy and supply-chain readiness. | `reviewed_gap_recorded` |
| `B38-PROD-M11` | P2 | Define rollback, removal and cache-recovery procedure. | `implemented` |

## Historical Planning Markers

These markers are preserved here only as compact routing anchors for tests and future discovery:

- B37: `T10-PLAN-M01..M03`, `T10-PLAN-M04..M05`, `T10-PLAN-M06`, `T10-PLAN-M07..M09`, `task_matrix_system_file_hygiene_owner_present`.
- Batch 35: `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr`.
- Batch 38: `B38-S1`, `B38-S2`, `B38-S3`, `B38-S4`, `B38-PILOT-NF01`, `blocked_pending_explicit_cache_mutation_approval`.
- Batch 39: `B39-S1`, `B39-S2`, `B39-S3`, `B39-S4`, `B39-S5`, `B39-TEST-M01..M54`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`.
- Batch 41: `B41-S1`, `B41-S2`, `B41-S3`, `B41-S4`, `B41-S5`, `B41-S6`, `B41-S7`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `first_run_guided_question_protocol_v1`, `first_run_answer_ledger_v1`, `first_run_ambiguous_route_intake_v1`, `batch41_s6_closure_packet_v1`, `first_run_cockpit_artifact_v1`, `closed_conditional_go_not_release_ready`.
- Batch 40: `B40-S2`, `B40-S3`, `B40-S4`, `B40-S5`, `manual_only`, `not_promoted`.

## Rollback

- Revert only files touched by the current slice.
- Preserve unrelated dirty changes.
- Do not use destructive git operations without explicit approval.
- For target-workspace pilots, rollback must be defined before mutation and must name owner, files, commands and stop condition.

## Verification

For docs/control-plane changes, run:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `git diff --check`

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

<!-- product-agent-os:end plan -->
