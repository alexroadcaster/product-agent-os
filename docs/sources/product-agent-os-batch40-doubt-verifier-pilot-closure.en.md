# Product-Agent OS Batch 40 S5 Doubt verifier pilot metrics and closure

Source status: `project-authored implementation evidence`. This packet is source-owned evidence for Batch 40 S5 and is not generated `site/` output.

## B40-S5 pilot metrics and closure packet

B40-S5 closes `B40-DVL-M22..M24` for the local Doubt / verifier loop by adding a deterministic `completion_skeptic_manual_pilot_ledger`, `completion_skeptic_scorecard_calibration` and `completion_skeptic_go_no_go_closure`.

Scope:

- pilot scope: `synthetic_local`.
- decision: `manual_only`.
- promotion status: `not_promoted`.
- release posture: `not_ready_for_automation_or_release`.
- no real project pilot, live server, browser automation, provider/API call, MCP server, Agents SDK runner, canonical graph mutation, external write, hook/automation activation or git action was performed.

## Pilot Ledger

`completion_skeptic_manual_pilot_ledger` records five synthetic-local rows so that the existing `min_sample_size: 5` scorecard threshold is met without pretending that three examples prove product value.

| pilot id | archetype | purpose | expected verifier behavior | attempt/failure/fix/retest |
| --- | --- | --- | --- | --- |
| `synthetic-pilot-1` | `docs_research` | Check source-sensitive documentation claims. | Catch unsupported or stale source claims and require fresh evidence or accepted gap. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-2` | `code_check` | Check a code/tool claim before saying done. | Require current command evidence, not user-claimed command output. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-3` | `expected_block` | Verify approval-bound action refusal. | Block pass/release claims when approval evidence is missing. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-4` | `docs_research` | Track a false positive candidate. | Keep false positives visible without turning them into rewrites. | attempt/failure/fix/retest recorded. |
| `synthetic-pilot-5` | `code_check` | Retest evidence sufficiency. | Confirm available command/source evidence and residual gaps. | attempt/failure/fix/retest recorded. |

Ledger fields:

- `pilot_denominators`: sample size, scenario mix, owner review status and no-unapproved-actions proof.
- `false_pass`: all rows false.
- `false_rewrite`: all rows false.
- `evidence_sufficient`: all rows true for the synthetic-local examples.
- `owner_accepted_gap`: one accepted metrics gap for synthetic-only calibration.
- `no_unapproved_actions`: true.

## Scorecard Calibration

`completion_skeptic_scorecard_calibration` wraps the existing scorecard and adds numerator/denominator evidence for promotion review:

| metric | numerator | denominator | note |
| --- | ---: | ---: | --- |
| `false_pass_rate` | 0 | 5 | No synthetic row allowed a false pass. |
| `false_rewrite_rate` | 0 | 5 | The loop may recommend revisions, but not unsupported rewrites. |
| `evidence_sufficiency_rate` | 5 | 5 | Synthetic examples include sufficient local evidence fields. |
| `missing_check_catch_rate` | 5 | 5 | Missing-check cases are caught. |
| `accepted_gap_rate` | 1 | 5 | One accepted metrics gap keeps synthetic scope explicit. |
| `user_revision_acceptance_rate` | 5 | 5 | Synthetic revision offers are accepted. |
| `revision_usefulness_rate` | 5 | 5 | Synthetic revisions are marked useful for calibration only. |

Calibration decision:

- `decision_status`: `calibrated_with_accepted_metrics_gap`.
- `promotion_policy`: `manual_only_synthetic_calibration_gap`.
- owner review status: `accepted_gap`.

This calibration is denominator-rich but still synthetic. It does not prove broad semantic usefulness, real user value, release readiness or automation readiness.

## Go/No-Go

`completion_skeptic_go_no_go_closure` records the final Batch 40 S5 decision:

- `decision_status`: `manual_only`.
- `promotion_status`: `not_promoted`.
- implemented rows: `B40-DVL-M22`, `B40-DVL-M23`, `B40-DVL-M24`.
- `rollback_disable_path`: keep `completion-skeptic` manual-only; remove candidate reminder/template references before any future activation.
- `next_approval_needs`: `exact_owner_approval_for_release_or_automation`, `exact_owner_approval_for_git_stage_commit_push_pr`, `exact_owner_approval_for_real_project_pilots`.

Blocked promotions without exact later approval:

- active automation.
- MCP server.
- Agents SDK runner.
- live provider/runtime call.
- browser automation.
- target workspace apply.
- canonical graph mutation.
- git stage/commit/push/PR or public/team release.

## Verification Contract

B40-S5 adds focused unit coverage for:

- `build_completion_skeptic_pilot_ledger`.
- `build_completion_skeptic_scorecard_calibration`.
- `build_completion_skeptic_go_no_go_packet`.
- `build_completion_skeptic_metrics_loop_record`.
- fixture checks `completion_skeptic_manual_pilot_ledger_present`, `completion_skeptic_scorecard_calibration_present` and `completion_skeptic_go_no_go_closure_present`.
- docs/control-plane sync for this packet, registry, Track 10 backlog, Track 10 plan, `RUNLOG.md`, `TEST.md` and `AGENTS.md`.

## Verification Evidence

Current run:

- focused B40-S5 code/docs contracts first failed on missing S5 helper API and missing source packet; after implementation they passed.
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`: 78 tests, `OK`.
- `python -m unittest discover -s tests -p "test_*.py" -v`: 871 tests, `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py`: exit `0`, `renderer_file_count: 197`, checks `completion_skeptic_manual_pilot_ledger_present`, `completion_skeptic_scorecard_calibration_present` and `completion_skeptic_go_no_go_closure_present` true.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json`: exit `0`, 26 sessions, 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`: `status: compatible`.
- strict MkDocs build: exit `0`.
- generated-site file-safe cleanup removed absolute `/en/` fallback links from English-original plan pages.
- `python tools\check_docs.py`: `OK`.
- `git diff --check`: exit `0`.

Generated `site/` was rebuilt for S5 because the new RU/EN source packet changed full-site i18n, search and sitemap inventory. Generated `site/` remains not source of truth.
