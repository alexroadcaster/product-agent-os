# TEST.md

<!-- product-agent-os:start test-plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-07

## Purpose

`TEST.md` is the compact verification routing layer for the current Product-Agent OS work. It should not store the full historical command ledger.

Verification evidence ownership is distributed as follows:

| TEST information class | Owning file now |
| --- | --- |
| Current verification commands and escalation rules | `TEST.md` |
| Current scope, acceptance and constraints | `REQUIREMENTS.md` |
| Active sequencing and rollback | `PLAN.md` |
| Current-cycle handoff and residual risks | `RUNLOG.md` |
| Current eval rubrics, thresholds and subjective gates | `EVALS.md` |
| Durable project rules and current operating status | `AGENTS.md` |
| Track 8 detailed scenario/methodology history | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 detailed methodology verification history | `docs/sources/product-agent-os-track-9-backlog.md` |
| Track 10 detailed execution verification history | `docs/sources/product-agent-os-track-10-backlog.md` |
| Source-backed claim and verification registry | `docs/sources/registry.md` |
| Batch 35 approval and execution packet | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Current Verification State

- Task 26 Batch 35 is closed through `T10-LIVE-M41` as `owner_closed_no_op_git_release_pr`.
- `T10-LIVE-M41` performed no git stage/commit/push/PR; future git write requires exact release branch or push target, commit message, PR base branch, PR title and intent, explicit branch/current-branch write approval and fresh preflight.
- B37-S1 docs/control-plane maintenance implements `T10-PLAN-M01..M03` and `T10-PLAN-M18` for the task-matrix contract, lifecycle/timestamp policy, `task-matrix-plan.md` placement policy and lightweight exception rule. B37-S2 implements `T10-PLAN-M04..M05` and `T10-PLAN-M17` for the checked-in `task-matrix-plan.md` template, renderer registration and packaging-surface evidence with `renderer_file_count: 195`. B37-S3 implements `T10-PLAN-M06`, `T10-PLAN-M10` and `T10-PLAN-M13` for `validate_task_matrix.py`, deterministic validator coverage, `task-matrix-validator-and-completion-report`, transcript/fixture guards and `task_matrix_validator_contract_present`. B37-S4 implements `T10-PLAN-M07..M09` and `T10-PLAN-M20` for planner routing, task-row handoffs, discovery signal classification and planning control governance with `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present` and `task_matrix_planning_control_governance_present`. B37-S5 implements `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16` and `T10-PLAN-M19` docs/source closure, compatibility policy, status/dashboard projection deferral, system-file hygiene ownership, lifecycle cleanup and Batch 37 closure; it records that `task-matrix-plan.md` is staged planning evidence only, not source truth or execution evidence.
- B38-S1 release gate/package metadata run covers `B38-PROD-M01..M03`: M01 remains `blocked_pending_explicit_git_release_fields`, M02 freezes checked-in package source with digest evidence and M03 records a local-only metadata exception while Codex compatibility returned `status: compatible`. This is not release readiness and does not authorize plugin install/cache mutation, live runtime/browser/provider work, canonical graph mutation or git stage/commit/push/PR.
- M41 post-B38 audit records `historical_preflight_snapshot`: Batch 35 `dirty_file_count: 15` is historical evidence, B37/B38/B38-S1 do not close M41, and a fresh git status/unrelated-change preflight is required before any git write.
- B38-S2 verification/install smoke run covers `B38-PROD-M04..M05`: M04 is implemented after full pre-install verification; M05 is `blocked_stale_plugin_cache_pending_refresh_approval` after read-only installed-cache inspection found stale visible cache. No plugin install/cache mutation, live runtime/browser/provider work, canonical graph mutation or git stage/commit/push/PR is authorized.
- B38-S3 real-project pilot design covers `B38-PROD-M06..M09`: first-run operator packet, target consent matrix, success metrics and dry-run evidence ledger are implemented as docs/source design artifacts. `no_real_project_execution_performed`; no live runtime/browser/provider work, target workspace mutation, canonical graph mutation, plugin-cache mutation or git stage/commit/push/PR is authorized.
- Latest Batch 35 current-run evidence is owned by `docs/sources/product-agent-os-batch35-approval-packet-draft.md`, `docs/sources/product-agent-os-track-10-backlog.md` and `docs/sources/registry.md`.
- Root `AGENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` are compact control-plane files. They preserve current routing and safety boundaries, not every historical batch result.

## Required Checks After Docs Or Control-Plane Changes

Run these after Markdown/source-registry/control-plane/test-contract edits:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

## Required Checks After Plugin Or Runtime Changes

Run focused tests for the touched module first. Then run the full Product-Agent OS verification set when plugin scripts, templates, fixture contracts, lifecycle skills, runtime behavior, CLI behavior or generated infrastructure contracts change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Use at least 20 minutes of command wait time for the full unittest command (`timeout_ms: 1200000`). Historical full-suite evidence in Track 10 shows exact 10-minute or shorter wrappers can create false timeouts and duplicate reruns.

## Runtime And External-Action Verification Boundaries

- Local live server launch, browser automation, provider/live external model/API calls, canonical graph mutation, git staging, commit, push and PR creation are approval-bound actions.
- If a slice is docs/control-plane/source-policy only, record why full unittest, fixture eval, transcript eval or strict MkDocs were not run.
- If runtime behavior changes, do not claim it works from code inspection alone. Run the relevant unit/integration/runtime checks and record evidence in the owning source packet.
- If generated artifacts are used as evidence, label them as generated orientation evidence unless the owning source document says otherwise.

## Historical Evidence Owners

- Track 8 scenario, compatibility, readiness and methodology hardening evidence: `docs/sources/product-agent-os-track-8-detailed-backlog.md`.
- Track 9 methodology intelligence evidence, including `T9-D1..T9-D12`, `T9-S`, `T9-R` and Task 22 closure: `docs/sources/product-agent-os-track-9-backlog.md` and `docs/sources/registry.md`.
- Track 10 Task 23 through Task 26 verification evidence, including Task 24 self-verification, Task 25 project graph and Task 26 live-layer batches: `docs/sources/product-agent-os-track-10-backlog.md` and `docs/sources/registry.md`.
- Batch 34 public docs, i18n, packaging and closure evidence: Track 10 backlog, source registry and the dedicated Batch 34 source packets under `docs/sources/`.
- Batch 35 M37-M41 approval-bound real testing evidence: `docs/sources/product-agent-os-batch35-approval-packet-draft.md`, source registry and Track 10 backlog.

## Verification For This TEST Maintenance

- Current run: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` first exposed stale historical `TEST.md`/`RUNLOG.md` assertions and a temporary mojibake risk after a mechanical rewrite; after UTF-8-safe restoration and compact ownership sync it ran 57 tests with `OK`. `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`.
- Current AGENTS compaction run: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 58 tests with `OK`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. Root `AGENTS.md` is compacted to durable rules and current operating status; historical implementation status, baseline command evidence and batch marker banks are owned by Track 8/9/10 source backlogs, registry entries and dedicated source packets.
- Current EVALS compaction run: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` first exposed stale historical `EVALS.md` aggregate expectations; after compact eval ownership sync it ran 59 tests with `OK`. `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. Root `EVALS.md` is compacted to current rubrics, thresholds, active eval routes, methodology eval map, unsupported-claim policy and historical evidence owner pointers.
- B37-S1 task-matrix contract run: new focused docs-test coverage first failed on missing B37-S1 markers. After implementing `T10-PLAN-M01..M03` and `T10-PLAN-M18`, `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 63 tests with `OK`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. Full unittest, fixture eval, transcript eval and Codex compatibility were not required for this slice because B37-S1 does not change plugin scripts, lifecycle skills, templates, renderer contracts, runtime behavior, CLI behavior or fixture contracts.
- B37-S2 task-matrix template and renderer run: RED coverage first failed on missing `.codex/artifact-templates/task-matrix-plan.md`, missing `artifact-task-matrix-plan` and stale fixture count. After implementation, `python -m unittest tests.product_agent_os.test_infrastructure_templates -v` ran 85 tests with `OK`; `python -m unittest tests.product_agent_os.test_infrastructure_renderer -v` ran 26 tests with `OK`; `python -m unittest tests.product_agent_os.test_fixture_eval_runner -v` ran 17 tests with `OK`; `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 64 tests with `OK`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 195`; `python -m unittest discover -s tests -p "test_*.py" -v` ran 821 tests with `OK`; transcript eval exited `0` with 17 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. The plugin cache remains stale until an explicit publication/cache refresh action is approved; no live automation, provider/live external model/API call, `.codex-plugin/plugin.json` mutation or git stage/commit/push/PR is authorized.
- B37-S3 task-matrix validator/eval run: RED coverage first failed on missing `validate_task_matrix_text`, `validate_task_matrix_file`, `validate_task_matrix.py`, `task-matrix-validator-and-completion-report`, transcript coverage, fixture checks and source-backed completion evidence. After implementation, focused validator tests ran 22 tests with `OK`; behavioral/transcript tests ran 6 tests with `OK`; fixture runner tests ran 17 tests with `OK`; infrastructure template tests ran 85 tests with `OK`; full unittest ran 828 tests with `OK`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 195`; transcript eval exited `0` with 18 sessions and 0 failures; Codex compatibility returned `status: compatible`. Fixture checks include `task_matrix_validator_contract_present`, `task_matrix_behavioral_eval_present`, `task_matrix_completion_report_guard_present`, `task_matrix_invalid_implemented_rows_blocked`, `task_matrix_detection_not_completion` and `task_matrix_summary_table_not_validator_target`.
- B37-S4 skill routing, discovery signal and planning control run: RED coverage first failed on missing planner/handoff/control-governance wording, discovery/audit/synthesis `task-matrix-plan.md` signal classification, missing behavioral case/session and missing fixture checks. After implementation, `python -m unittest tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_audit -v` ran 176 tests with `OK`; `python -m unittest tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixture_eval_runner -v` ran 23 tests with `OK`; `python -m unittest discover -s tests -p "test_*.py" -v` ran 835 tests with `OK`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 195` and the S4 `task_matrix_*` checks true; transcript eval exited `0` with 19 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. Fixture checks include `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present` and `task_matrix_planning_control_governance_present`; behavioral evals include `task-matrix-agent-handoff-and-planning-control`; no hook activation, recurring automation, MCP, Agents SDK runner, live server/browser automation, provider/live external model/API call, canonical graph mutation or git stage/commit/push/PR was performed.
- B37-S5 docs, projection, hygiene, lifecycle and closure run: RED docs contract first failed on missing S5 markers; focused integration tests ran 174 tests with `OK`; `python -m unittest discover -s tests -p "test_*.py" -v` ran 841 tests with `OK`; `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with `renderer_file_count: 195` and `task_matrix_projection_deferred_in_b37`; transcript eval exited `0` with 19 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. Strict MkDocs was not run because S5 did not change MkDocs navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search, sitemap or generated `site/` evidence. No hook activation, recurring automation, MCP, Agents SDK runner, live server/browser automation, provider/live external model/API call, canonical graph mutation or git stage/commit/push/PR is authorized.
- B37-S5 markers: `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- B38-S1 release gate/package metadata run: RED focused docs contract first failed on missing B38-S1 source/control-plane markers; package evidence used `git status --short`, `git ls-files plugins/product-agent-os`, ignored-cache check, deterministic digest calculation and `.codex-plugin/plugin.json` review; Codex compatibility returned `status: compatible`; after source/control-plane sync, `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 71 tests with `OK`, `python tools\check_docs.py` returned `OK: documentation structure checks passed`, and `git diff --check` exited `0`. strict MkDocs was not run because S1 does not change MkDocs navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search, sitemap or generated `site/` evidence.
- T10-LIVE-M41 post-B38 audit run: RED focused docs contract first failed on missing `historical_preflight_snapshot`, stale `Next executable product action` wording and missing source/control-plane registry markers. After source/control-plane sync, focused M41 docs contract passed, `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 72 tests with `OK`, `python tools\check_docs.py` returned `OK: documentation structure checks passed`, and `git diff --check` exited `0`. strict MkDocs was not run because this audit does not change MkDocs navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search, sitemap or generated `site/` evidence.
- B38-S2 verification/install smoke run: RED focused docs contract first failed on missing B38-S2 source/control-plane markers. `B38-PROD-M04` verification ran `python -m unittest discover -s tests -p "test_*.py" -v`; full unittest ran 846 tests with `OK`; fixture eval exited `0`; transcript eval exited `0` with 19 sessions and 0 failures; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`, `python tools\check_docs.py` returned `OK: documentation structure checks passed`, and `git diff --check` exited `0`. `B38-PROD-M05` plugin cache inspection found stale installed cache: `plugin_install_smoke_status: read_only_inspection_completed_stale_cache_detected`, 10 visible cache skills vs 11 checked-in skills, missing `docs-maintainer`, 32 visible cache script files vs 84 checked-in script files and 34 visible cache template files vs 202 checked-in template files. `plugin_cache_refresh_status: blocked_pending_explicit_cache_mutation_approval`; no plugin install/cache mutation was performed. strict MkDocs was not run because this slice does not change MkDocs navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search, sitemap or generated `site/` evidence.
- B38-S3 real-project pilot design run: source/control-plane sync adds `docs/product-agent-os/real-project-pilot.md` and `.en.md`, MkDocs navigation/check-docs registration, Track 10 backlog and registry evidence for `B38-PROD-M06..M09`. Focused B38-S3 docs contract passed; strict MkDocs ran through a workspace-local ignored venv at `tmp\mkdocs_venv_b38s3` and exited `0`; generated `site/` was rebuilt and mechanically normalized for file-safe English-original fallback links plus trailing whitespace; final `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 74 tests with `OK`; `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`. The real project pilot execution was not run; no target workspace mutation, plugin-cache mutation, live server, browser automation, provider/API call, canonical graph mutation, external write or git action was performed.
- Focused docs contract: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`.
- Documentation structure: `python tools\check_docs.py`.
- Diff hygiene: `git diff --check`.
<!-- product-agent-os:end test-plan -->
