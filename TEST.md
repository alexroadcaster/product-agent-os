# TEST.md

<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`TEST.md` is the compact verification routing layer. It defines current checks, escalation boundaries and evidence owners. Detailed historical command logs and batch-specific command archives belong in [current control-plane state](docs/product-agent-os/control-plane-current-state.md), source backlogs, evidence packets and `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Run these checks after changes to root control-plane files, docs/source registry, templates or test contracts:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes. Full discovery remains the broad route:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Required Checks After Plugin Or Runtime Changes

Use focused checks first, then broaden through the relevant project route:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

Use `timeout_ms: 1200000` for full Product-Agent OS unittest runs.

## Current Verification State

| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| Batch 39 | `B39-S1` through `B39-S5` are source-owned; S5 is `closed_for_owner_feedback_testing_not_release_ready`. | Use `prod_test.md`, S5 packets, focused tests, full unittest, fixture/transcript eval, Codex compatibility, docs check and diff hygiene before stronger claims. |
| Batch 41 | S9 modernization and Neural_Flow comparison are generated-artifact evidence. | Use focused first-run/cockpit renderer tests and docs checks; browser/Cosmos.gl/WebGL/target-apply proof requires approval. |
| Batch 42 | Planned-only matrix. | No fixed-auto-engagement claim until route/eval/source/cache/session evidence exists. |
| Batch 44 | Self-Learning Loop S0-S7 are local/staged/manual evidence. | Run focused state/extensions/docs tests before S8 decision; no automation claim without owner approval and activation proof. |
| Batch 45 | T21 cost-waived run records one approved primary call followed by strict-schema abort; T22-A02 records no-go because T21 has no valid pairs and reviewer gate was not run; advisory-only/no-go remains active and T14 positive signal remains below threshold. | Run focused coding-standards/comment-sufficiency/docs checks for local changes; any future baseline/treatment/model/reviewer run requires strict output/schema normalization, a new exact approval and a valid T21 result before T22 reviewer gate. |
| Track 11 DOC-M25 | Root `site`, search and sitemap freshness are source-owned by DOC-M25 packet. | Root site freshness checks prove generated site/search/sitemap only; browser proof and broad scans remain separate. |
| GPT-5.6 `.codex` remediation | R1-R6 current evidence: agent validator 15/15 with zero config errors; focused contracts 184 OK; docs 100 OK; hooks 19 OK plus both hook validators; strict doctor 0 fail; fixture eval exit 0; transcript eval 26/26; compatibility `compatible`; full discovery 1195 OK with 1 skip; docs structure OK. Source: `docs/superpowers/plans/2026-08-05-gpt56-r1-r6-remediation.md`. | Maintain final diff/task-plan hygiene. Separately restart Codex for fresh MCP/`SessionStart` activation proof and run same-effort/one-lower-effort behavioral comparisons before promotion. |

## Batch-Specific Check Routes

| Batch or route | Compact check route | Evidence owner |
| --- | --- | --- |
| Batch 39 | `prod_test.md` attempt ledger, focused schema/collector/dashboard/route tests, fixture eval, transcript eval, Codex compatibility, docs check, diff hygiene. | `prod_test.md`; B39 packets. |
| Batch 44 | `python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions -v`, staged initializer/runner/export checks as scoped by packet, docs check, diff hygiene. | B44 packets; `docs/product-agent-os/self-learning-loop.md`. |
| Batch 45 Professional Code Authoring | Focused `test_comment_sufficiency`, `test_batch45_s3_professional_code_authoring`, `test_coding_standards_artifacts`, automation/self-learning tests where touched, docs check, diff hygiene. | B45 packets; `docs/product-agent-os/coding-standards.md`. |
| Batch 45 retest/post-Q4 | `python -m json.tool` for changed B45 packets, including `docs\superpowers\specs\batch45-postq4-t17-frozen-heldout-corpus.json`, `docs\superpowers\specs\batch45-postq4-t18-promotion-grade-eval-design.json`, `docs\superpowers\specs\batch45-postq4-t19-cost-timeout-retention-policy.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-results.json` and `docs\superpowers\specs\batch45-postq4-t22-promotion-grade-decision-packet.json`, `python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v`, `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`, docs check, diff hygiene. | Q0-Q4 and T01-T22 packets. |
| Track 11 docs toolchain | Project-local `.venv-docs`, `.docs-tools/node`, `.docs-tools/bin`, `.docs-tools/reports`, `docs/assets/javascripts/vendor` checks only within approved scopes. | Track 11 plan and DOC-M34..DOC-M41 packets. |

## Control-Plane Size Budgets

Root control-plane files use a compactness budget. `RUNLOG.md` keeps the historical `50 KB` (`50 * 1024` UTF-8 bytes) guard; the same overflow discipline applies to `PLAN.md`, `TEST.md`, `EVALS.md` and `REQUIREMENTS.md`. If a required update would exceed the budget, run `.codex/workflows/control-plane-sync.md` as `overflow_refactor_required`: route scope to `REQUIREMENTS.md`, sequencing to `PLAN.md`, verification to `TEST.md`, eval/claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, then keep root files as current pointers.

## MkDocs Runtime Location

Use the project-local docs runtime for current docs checks:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict
```

The default `python` may not have MkDocs installed. Historical fallback paths such as `C:\tmp\codex_docs_mkdocs` or `tmp\mkdocs_deps_b40s4` are historical evidence only.

## Runtime And External-Action Verification Boundaries

Fresh explicit approval is required before:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries.

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/sources/product-agent-os-track-10-backlog.md`, `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/sources/product-agent-os-track-10-backlog.md`, `docs/product-agent-os/control-plane-current-state.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `prod_test.md`, B39 packets |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/sources/product-agent-os-track-10-backlog.md` |
| `B41-S1..S9` | B41 packets and Track 10 backlog |
| `B42-S1..S5` | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json` |
| `B44-S0..S7` | B44 packets and Track 11 plan |
| `B45-PCA-M24..M27`, `B45-PCA-M37-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02` | B45 packets, Track 11 plan and registry |
| `DOC-M34..DOC-M41`, `DOC-M25` | Track 11 plan and documentation-refresh packets |
| Track 8 / Track 9 / Track 10 | `docs/sources/product-agent-os-track-8-detailed-backlog.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/product-agent-os-track-10-backlog.md` |
| Source registry | `docs/sources/registry.md`, `docs/sources/registry.en.md` |

## Compatibility Anchors

Compact route anchors: `B37-S1`, `T10-PLAN-M01..M03`, `T10-PLAN-M18`, `task-matrix contract`, `task-matrix-plan.md`, `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `B42-S1..S5`, `B44-S0` through `B44-S7`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->
