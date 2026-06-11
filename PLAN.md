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
- Preserve unrelated dirty work and record only the evidence needed for current handoff.

## Current State

| Workstream | State | Planning impact |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned and closed for completed historical slices. | Use backlogs and registry for historical detail. |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no branch, stage, commit, push or PR. | Future git-write work needs fresh preflight and exact approval. |
| Batch 38 package-source/readiness | Implemented/recorded. `B38-S2` current cache evidence is `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat prior blockers as historical evidence, not current active blockers unless the same condition recurs. |
| `B38-PILOT-NF01` | Docs-only target addendum completed; target apply blocked by `source_policy_status: blocked` and missing target control-plane/source registry artifacts. | Do not mutate target project until source policy and artifacts are resolved. |
| Batch 39 | Executing through `prod_test.md`; `B39-S1` foundational local contracts `B39-TEST-M01..M10` have current local evidence and `B39-TEST-M11` is next. | Continue only through per-test attempt/failure/fix/retest evidence; no readiness claim until the full Batch 39 gate set is satisfied. |
| Batch 40 completion-skeptic | Local manual foundation closed; automation status `manual_only` and `not_promoted`. | Keep automation promotion candidate-only until gates are satisfied. |
| Agent control-plane sync | Current project agents and Product-Agent OS templates now require `.codex/workflows/control-plane-sync.md` before Completion Brief. | Future Product-Agent OS tasks must update owned control-plane files or record `not_applicable` / `handoff_required`; no hook or automation was activated. |

## Next Implementation Queue

| Slice | Scope | Owner action | Codex action | Verification |
| --- | --- | --- | --- | --- |
| `B39-S1` | Foundational local evidence package closed for `B39-TEST-M01..M10`. | Review only if S1 evidence needs rework. | Preserve S1 artifacts as source evidence; do not promote to readiness by themselves. | `prod_test.md` attempt rows, focused tests and synthetic artifacts exist; no target mutation occurred. |
| `B39-S2` | Run first approved Batch 39 test subset, starting with `B39-TEST-M11`. | Provide/approve target, credentials-free setup and manual observations where needed. | Execute only approved read/write steps, record attempt/failure/fix/retest ledger. | Deterministic commands and manual evidence recorded in `prod_test.md`. |
| `B39-S3` | Fix issues found by first subset. | Approve scoped edits if fixes require mutation. | Implement focused fixes, preserve unrelated dirty changes, update evidence. | Relevant tests/checks rerun; accepted gaps explicit. |
| `B39-S4` | Retest and risk review. | Confirm product acceptance or residual risk tolerance. | Rerun failed checks, prepare risk/readiness summary. | Supported/unsupported claims separated. |
| `B39-S5` | Closure and next-route decision. | Decide continue, pause, promote, or replan. | Update control-plane handoff and source registry if required. | No readiness claim without current-run evidence or accepted gap. |

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
- Batch 39: `B39-S1`, `B39-S2`, `B39-S3`, `B39-S4`, `B39-S5`, `B39-TEST-M01..M54`.
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
