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

- Task 26 Batch 35 is complete through `done_through_m40`.
- `T10-LIVE-M41` remains `blocked_pending_explicit_git_release_fields`; no git stage/commit/push/PR is allowed until the owner provides exact release branch or push target, commit message, PR base branch, PR title and intent, and explicit branch/current-branch write approval.
- B37-S1 docs/control-plane maintenance implements `T10-PLAN-M01..M03` and `T10-PLAN-M18` for the task-matrix contract, lifecycle/timestamp policy, `task-matrix-plan.md` placement policy and lightweight exception rule. B37-S2 implements `T10-PLAN-M04..M05` and `T10-PLAN-M17` for the checked-in `task-matrix-plan.md` template, renderer registration and packaging-surface evidence with `renderer_file_count: 195`.
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
- Focused docs contract: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`.
- Documentation structure: `python tools\check_docs.py`.
- Diff hygiene: `git diff --check`.
<!-- product-agent-os:end test-plan -->
