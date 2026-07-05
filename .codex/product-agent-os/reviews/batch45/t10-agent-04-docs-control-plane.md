# B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET: docs/control-plane sidecar

Source status: project-local docs/control-plane review packet; inspection-only. No source, registry, test, root control-plane, runtime, provider, browser, target, git, release, deploy or automation action was performed.

## Scope

- Task: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`.
- Role: Docs Maintainer / control-plane sidecar.
- Allowed write: this report only.
- Subagents: none launched; the task is a single-file sidecar with shared control-plane ownership.
- Files read:
  - `.codex/config.toml`
  - `.codex/workflows/task-plan-lifecycle.md`
  - `.codex/workflows/control-plane-sync.md`
  - `PLAN.md`
  - `TEST.md`
  - `EVALS.md`
  - `RUNLOG.md`
  - `docs/sources/registry.md`
  - `docs/sources/registry.en.md`
  - `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
  - `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
  - `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`
  - `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`
  - `tests/product_agent_os/test_coding_standards_artifacts.py`
  - `.codex/product-agent-os/lifecycle-state.json`
  - prior sidecars `.codex/product-agent-os/reviews/batch45/t06-agent-04-docs-control-plane.md` and `t11-agent-04-docs-control-plane.md`

## Current source boundary

T10 is recommended but not implemented:

- `docs/superpowers/specs/batch45-post-q4-next-tasks.json` defines `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET` as `approval_packet_only`, `recommended_before_any_new_t05b_run`.
- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json` routes T10 as the required redesign before any behavior-proof rerun.
- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json` explicitly says T10 is required before any approved rerun.
- Existing compact root state says: Q4 `14`; T01-T03 `14 -> 0`; T05 timeout; T06/T08 no-go; T11 source-only. No target/runtime/CI proof.
- No registry marker for `B45-POSTQ4-T10-A01` exists yet.

## Exact source-owned packet path

Create the primary T10 packet at:

- `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json`

Recommended fields:

- `schema_version`: `batch45_postq4_t10_live_eval_harness_redesign_packet_v1`
- `task_id`: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- `evidence_id`: `B45-POSTQ4-T10-A01`
- `status`: `implemented_approval_packet_only_not_run`
- `route`: `approval_packet_only`
- `source_status`: project-authored approval packet only; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action
- `basis`: T05 result, T05B packet, T06 decision, T08 architecture next-actions, T11 source design
- `harness_problem`: T05 baseline-first stop-on-timeout erased treatment and reviewer comparison
- `redesigned_routes`: `strict_stop_on_timeout`, `paired_continue_with_invalid_pair_quarantine`, `retry_on_timeout_with_owner_cap`, `diagnostic_only`
- `recommended_default_route`: `paired_continue_with_invalid_pair_quarantine`
- `per_task_pairing_contract`: baseline/treatment pair id, order, timeout status, no-op status, validity status, reviewer timing
- `timeout_policy`: per-task timeout, total cap, process-tree kill, retry cap, invalid-pair quarantine
- `reviewer_timing`: reviewer runs only on valid comparable pairs, or records diagnostic-only gap
- `cost_cap_contract`: owner-filled max cost, call cap, stop condition and accepted-gap path
- `privacy_retention_contract`: raw outputs temp-only, sanitized rollup only in repo
- `abort_conditions`: no exact owner approval, provider/model mismatch, cost cap missing, raw output retention risk, target write risk, process-stop failure
- `promotion_threshold_candidate`: comparable-pair count, improvement threshold, pairwise win/equal floor, reviewer decision, timeout/no-op exclusion and static-warning non-promotion rule
- `control_plane_sync_decision`
- `no_unapproved_actions`
- `unsupported_claims`
- `verification`

## Registry markers

Add one compact paired marker after the packet exists.

`docs/sources/registry.md`:

```text
- Product-Agent OS Track 11 Batch 45 post-Q4 T10 live eval harness redesign packet with `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET` / `B45-POSTQ4-T10-A01`, route `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json` (checked_at=2026-07-05, trust=high for source-owned approval-packet-only harness redesign after T05 timeout, T06/T08 no-go and T11 source-only design; separates timeout/paired/retry/diagnostic routes and requires fresh exact owner approval before any live/model/provider call; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
```

`docs/sources/registry.en.md`:

```text
- Product-Agent OS Track 11 Batch 45 post-Q4 T10 live eval harness redesign packet with `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET` / `B45-POSTQ4-T10-A01`, route `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json` (checked_at=2026-07-05, trust=high for source-owned approval-packet-only harness redesign after T05 timeout, T06/T08 no-go and T11 source-only design; separates timeout/paired/retry/diagnostic routes and requires fresh exact owner approval before any live/model/provider call; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
```

## Track 11 row

Update the existing Track 11 Batch 45 table row for T10 near T08/T11:

```text
| `B45-POSTQ4-T10` | P1 | `B45-S7` | Redesign the live eval harness approval packet before any new T05B-style rerun. | `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json`; `docs/superpowers/specs/batch45-post-q4-next-tasks.json`; lifecycle marker; focused tests; registry/control-plane sync. | Define paired baseline/treatment continuation, invalid-pair quarantine, retry/diagnostic-only options, timeout/process-kill, reviewer timing, cost cap, temp-only retention and abort conditions. | T08 and T11 require T10 before any future approved behavior rerun. | Packet-only; no live/model/provider call; no M26/M35/T05/T06 reversal. | `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`; docs checks; `git diff --check`. | Stop before live/model/provider/API, runtime/browser, target command/mutation, database, CI/blocker, git/release/deploy/automation. | `implemented_B45_POSTQ4_T10_harness_redesign_packet_only: B45-POSTQ4-T10-A01`; `new_exact_approval_required_before_rerun`; `invalid_pairs_do_not_promote` |
```

Add a compact historical marker:

```text
`batch45_professional_code_authoring_post_Q4_T10_live_eval_harness_redesign`: `B45-POSTQ4-T10-A01` records the approval-packet-only redesign in `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json`. It converts the brittle T05 baseline-first stop-on-timeout route into explicit strict-stop, paired-continue, retry-on-timeout and diagnostic-only choices, with invalid-pair quarantine, process-stop, cost, reviewer and temp-only retention boundaries. It performs no live/model/provider call and does not reverse M26/M35/T05/T06.
```

## Root control-plane pointers

Use terse root changes only:

- `PLAN.md`: update the Batch 45 post-Q4 row to include `B45-POSTQ4-T10-A01`; state "T10 approval-packet-only harness redesign; no rerun authorized".
- `TEST.md`: add `B45-POSTQ4-T10-A01` to the existing Batch 45 retest/post-Q4 list; keep the same focused command block unless the packet introduces a deterministic JSON validator.
- `EVALS.md`: extend the Batch 45 Q0-Q4/post-Q4 sentence with "T10 approval-packet-only harness redesign; no target/runtime/CI proof and no live rerun approval".
- `RUNLOG.md`: do not expand. If a current-cycle handoff pointer is unavoidable, replace an existing Batch 45 pointer rather than appending narrative.
- `REQUIREMENTS.md`: `not_applicable` unless T10 changes product scope or acceptance criteria.
- `prod_test.md`: `not_applicable`; Batch 39 surface.

## Lifecycle marker

During actual T10 implementation, update `.codex/product-agent-os/lifecycle-state.json` after the visible Task Brief:

- `task_start_brief_shown`: `true`
- `task_id`: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- `scope`: `Create approval-packet-only live eval harness redesign; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action.`
- `brief_schema_version`: `task_start_brief_v1`
- `brief_format`: `field_list`
- `brief_fields_present`: all Task Brief fields from `.codex/workflows/task-plan-lifecycle.md`
- `completion_status`: `implemented_approval_packet_only_not_run`
- `closure_level`: `docs_contract_ready_live_eval_harness_redesign_no_run`
- `completion_gaps`: T10 is not a rerun, not behavior proof, not promotion approval

This sidecar did not update the marker because the user allowed writing exactly this report file.

## Test assertions

Add `POST_Q4_T10_HARNESS = DOCS / "superpowers" / "specs" / "batch45-postq4-t10-live-eval-harness-redesign-packet.json"` and a focused test such as `test_b45_postq4_t10_live_eval_harness_redesign_is_packet_only`.

Recommended assertions:

- T10 packet exists and parses as JSON.
- Packet fields equal:
  - `schema_version == "batch45_postq4_t10_live_eval_harness_redesign_packet_v1"`
  - `task_id == "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET"`
  - `evidence_id == "B45-POSTQ4-T10-A01"`
  - `status == "implemented_approval_packet_only_not_run"`
  - `route == "approval_packet_only"`
- `redesigned_routes` contains:
  - `strict_stop_on_timeout`
  - `paired_continue_with_invalid_pair_quarantine`
  - `retry_on_timeout_with_owner_cap`
  - `diagnostic_only`
- Recommended default is `paired_continue_with_invalid_pair_quarantine`.
- Static warning delta cannot promote.
- Invalid, timeout, no-op and missing-treatment pairs cannot count as promotion evidence.
- Fresh exact owner approval is required before any live/model/provider/API call.
- Raw outputs in repo are forbidden; sanitized rollup only is allowed.
- `no_unapproved_actions` values are all `false`.
- Decision flags are all false for:
  - `m26_reversed`
  - `m35_reversed`
  - `t05_timeout_reversed`
  - `promotion_allowed`
  - `live_model_rerun_allowed_without_new_approval`
  - `runtime_browser_or_target_claim_allowed`
  - `ci_blocker_automation_allowed`
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json` records:
  - `latest_t10_harness_redesign == "docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json"`
  - T10 in `execution_update.executed_task_ids`
  - `status_by_task["B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET"] == "implemented_approval_packet_only_not_run"`
- `docs/sources/registry.md` and `docs/sources/registry.en.md` contain:
  - `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
  - `B45-POSTQ4-T10-A01`
  - `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json`
  - no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof wording
- `PLAN.md`, `TEST.md`, `EVALS.md` and Track 11 plan contain compact `B45-POSTQ4-T10-A01` pointers.
- `RUNLOG.md` should not be required for detailed T10 assertions.
- Lifecycle assertion should require `task_id == "B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET"` only in the actual T10 implementation slice, not in this sidecar-only report.

Recommended command gate after implementation:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Strict MkDocs is not required unless T10 changes navigation, public docs, Markdown extensions, Mermaid, generated `site`, search, sitemap or docs-tooling config.

## Compact size observations

Measured in this review:

- `RUNLOG.md`: `51123` bytes against the configured `50 * 1024 = 51200` byte budget; only 77 bytes remain.
- `PLAN.md`: `49695` bytes.
- `TEST.md`: `49935` bytes.
- `EVALS.md`: `49926` bytes.
- `docs/sources/registry.md`: `99440` bytes.
- `docs/sources/registry.en.md`: `99403` bytes.
- Track 11 plan: `204703` bytes.
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`: `22566` bytes.
- `tests/product_agent_os/test_coding_standards_artifacts.py`: `71569` bytes.

Conclusion: detailed T10 design belongs in the source-owned JSON packet; root files should get single-line pointers only. Do not expand `RUNLOG.md`.

## Control-plane sync decision

```yaml
control_plane_sync_decision:
  REQUIREMENTS.md: not_applicable_no_scope_or_acceptance_change_seen
  PLAN.md: handoff_required_compact_t10_status_pointer_after_packet
  TEST.md: handoff_required_compact_t10_route_pointer_after_packet
  EVALS.md: handoff_required_compact_t10_claim_ceiling_after_packet
  RUNLOG.md: handoff_required_due_runlog_budget_do_not_expand
  prod_test.md: not_applicable_batch39_surface
  docs/sources/registry.md: handoff_required_t10_route_marker_after_packet
  docs/sources/registry.en.md: handoff_required_t10_route_marker_after_packet
  docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md: handoff_required_t10_row_and_marker_after_packet
  .codex/product-agent-os/lifecycle-state.json: handoff_required_only_during_actual_t10_execution
```

## Unsupported claims to keep out

- `live_model_rerun_performed`
- `real_ai_agent_behavior_improvement`
- `M26_no_go_reversed`
- `M35_no_go_reversed`
- `T05_timeout_reversed`
- `promotion_ready`
- `ci_workflow_readiness`
- `blocker_enforcement_readiness`
- `active_automation_readiness`
- `runtime_browser_readiness`
- `target_workspace_apply_safety`
- `provider_or_live_api_behavior`
- `release_deploy_publish_readiness`
- `root_site_freshness`
- `raw_outputs_retained_in_repo`

## Verification

This report is inspection-only. Commands used:

- `Get-Content`, `Get-Item`, `Get-ChildItem`, `rg`, `git status --short`.

Not run by design:

- unit tests
- docs checks
- `git diff --check`
- MkDocs
- provider/model calls
- runtime/live server
- browser automation
- target workspace commands
- git actions

## Completion Brief

- Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET docs/control-plane sidecar`
- Result status: `inspection_only_report_written`
- What was done: inspected compact control-plane and Batch 45 T05/T05B/T08/T11 patterns; recommended exact T10 packet path, registry markers, Track 11 row, root pointers, lifecycle marker fields and test assertions.
- Files / artifacts changed: `.codex/product-agent-os/reviews/batch45/t10-agent-04-docs-control-plane.md` only.
- Verification evidence: read-only inspection commands listed above; no implementation checks were run because this slice writes only the sidecar report.
- Residual risks / accepted gaps: actual T10 packet and root/registry/test sync remain handoff-required; lifecycle marker was not updated due the one-file write constraint; root files are near compactness limits.
- Follow-up: Builder/Tester or Docs Maintainer should implement the T10 source-owned JSON packet and compact sync in a separate slice.
