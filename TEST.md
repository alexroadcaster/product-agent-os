# TEST.md

<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`TEST.md` is the compact verification routing layer. It defines which checks are required for current docs, control-plane, plugin/runtime, eval and Batch 39 work. Detailed historical evidence belongs in source-owned backlogs, eval reports, `RUNLOG.md` or `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Run these checks after changes to root control-plane files, docs/source registry, templates or test contracts:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
python -m unittest discover -s tests -p "test_*.py" -v
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

## Required Checks After Plugin Or Runtime Changes

Use focused checks first, then broaden through the relevant project route:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest discover tests -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

If a slice changes Product-Agent OS plugin behavior, also inspect the matching fixture/eval/transcript checks referenced by the source plan or backlog before making readiness claims.

Use `timeout_ms: 1200000` for full Product-Agent OS unittest runs.

## Batch 39 Verification Contract

- `prod_test.md` is the required attempt/failure/fix/retest ledger for `B39-TEST-M01..M54`.
- Future Batch 39 pilots should include real-project target evidence where it improves Product-Agent OS confidence. Internal `codex_docs` fixtures remain valid for deterministic contracts, but they do not replace real target discovery when the route depends on project shape, source policy, runtime signals or user workflow.
- Every Batch 39 task must record:
  - setup and prerequisites;
  - owner action and Codex action;
  - exact command/manual step;
  - observed evidence;
  - result status;
  - failure, fix and retest loop if applicable;
  - residual risk or accepted gap.
- Do not treat a planned test matrix as execution evidence.
- Do not treat generated dashboards, generated reports or project graphs as proof unless backed by source artifacts, current command evidence, current runtime evidence or an explicit accepted gap.

## Runtime And External-Action Boundaries

Runtime And External-Action Verification Boundaries

Fresh explicit approval is required before:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries. Build/test/runtime/browser/provider/database/git/release actions require exact approval before execution.

## Current Verification State

| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` current evidence records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| `B38-PILOT-NF01` | Docs-only pilot addendum; target apply blocked by `source_policy_status: blocked`. | Resolve target source policy and target control-plane artifacts before target mutation. |
| Batch 39 | `B39-S1` foundational local contracts, `B39-S2` archetype/first-run/three-target evidence, `B39-TEST-M21-A01..A03`, route accuracy through `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33` functional regression/repeatability and `B39-S4` hardening are current through `B39-S4-REMAINING-GATES-A01`. S4 evidence includes all-script `--help` matrix at 32/32, SOL / Neural_Flow static dependency readiness, graph-depth, security/privacy, templates, skills/subagents, MCP boundary, onboarding, cross-platform, source freshness, HTML usability, LLM-judge, retention, incident/recovery and release-governance contract evidence. Current verification passed focused S4 tests, graph-analysis regression tests, docs contract, fixture eval, transcript eval, Codex compatibility, docs check, diff hygiene and full unittest discovery 983 OK / 1 skipped. No release/readiness claim yet. | Continue with `B39-S5` closure/go-no-go and owner-feedback testing. Preserve fixed S4 blocker tests, graph-depth regression gates and `python -m unittest tests.product_agent_os.test_batch39_s4_hardening -v`. |
| Batch 40 completion-skeptic | Local manual loop closed as `manual_only` and `not_promoted`. | Automation promotion requires manual success evidence, eval cases, owner, cadence, stop condition and rollback/disable path. |
| Agent lifecycle and control-plane sync | Current local agents, packaged agent templates, workflows, config templates and `agent-context-contract` require config-routed Task Brief / Completion Brief plus control-plane sync before completion; current verification passed. | Rerun task lifecycle, infrastructure template, docs, docs-structure and diff hygiene checks after future changes to this contract. |

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `PLAN.md`, `prod_test.md` |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| Track 8 | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 | `docs/sources/product-agent-os-track-9-backlog.md` |
| Source registry | `docs/sources/registry.md` |
| Batch 35 | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Compatibility Marker Bank

- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- B38-S1 release gate/package metadata run; focused docs contract; Codex compatibility returned `status: compatible`; strict MkDocs was not run.
- M01 is owner-closed as no-op after historical missing release fields; M02 freezes the checked-in package source; M03 records the owner decision to keep Product-Agent OS local-only/internal R&D.
- M41 post-B38 audit; historical_preflight_snapshot; fresh git status/unrelated-change preflight; B37/B38/B38-S1 did not themselves close M41.
- B38-S2 verification/install smoke run; full unittest ran 846 tests with `OK`; fixture eval exited `0`; transcript eval exited `0` with 19 sessions and 0 failures; plugin cache inspection found stale installed cache; plugin_cache_refresh_attempt_status: blocked_sandbox_cache_write_denied_after_backup_stage; local_cache_refresh_result: REFRESH_OK; target_cache_still_stale: false.
- B38-S3 real-project pilot design run; docs contract; strict MkDocs; real project pilot execution was not run.
- B38-S4 safety and rollback run; validate_source_policy.py; validate_system_file_hygiene.py; secret_like_findings: 6; validate_codex_compatibility.py; not a security certification; No cache/global config mutation.
- B38-PILOT-NF01 `Neural_Flow` target pilot run; detect_project.py; run_methodology_audit.py; run_codex_runtime_runner.py; render_infrastructure.py --stage; scan_project_code_graph.py --stage; validate_source_policy.py; source_policy_status: blocked; false `pr_review` route; 481 nodes; Dashboard aggregation remains incomplete; staged hooks require exact approval; secret_like_findings: 0; No target mutation.
- B40-S4 implements Doubt / verifier loop docs/site/source-transfer; strict MkDocs.
- B40-S5 implements Doubt / verifier loop pilot metrics and closure; completion_skeptic_manual_pilot_ledger; completion_skeptic_go_no_go_closure.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->
