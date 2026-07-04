# B45-POSTQ4-T06-PROMOTION-DECISION: docs/control-plane sync review

Source status: project-local inspection-only review packet.

Review ID: `B45-POSTQ4-T06-agent-04-docs-control-plane`
Role: Docs Maintainer / control-plane sync reviewer
Created at: 2026-07-04
Scope: inspect current control-plane and source-registry state for `B45-POSTQ4-T06-PROMOTION-DECISION`; do not mutate core files.

## Decision

T06 should record a compact no-go / keep-advisory-only promotion decision unless a new exact owner approval runs T05B and produces complete comparable live/model evidence.

Current source evidence does not support promotion:

- T01-T03 reduced copied-fixture static advisory warnings from `14 -> 0`, but static warning reduction is not behavior proof.
- T05 used the exact-approved live/model rerun surface, completed 1 baseline task, timed out on 1 baseline task, stopped the remaining 14 primary runs and did not run treatment or reviewer comparison.
- T05B is approval-packet-only and explicitly requires a new exact owner approval before any live/model/provider call.
- Existing blockers from `B45-PCA-M26`, `B45-PCA-M27`, `B45-PCA-M35` and `B45-PCA-M37-A01` remain active.

## Files Inspected

- `PLAN.md`
- `TEST.md`
- `EVALS.md`
- `docs/sources/registry.md`
- `docs/sources/registry.en.md`
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
- `.codex/product-agent-os/lifecycle-state.json`
- supporting source packets:
  - `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
  - `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
  - `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`

## Current Alignment

`PLAN.md` already has compact routing for post-Q4 T01-T05B. It says T06 can record no-go or wait for a new exact T05B approval. It does not yet expose a completed T06 marker.

`TEST.md` already routes Batch 45 post-Q4 checks through focused comment-sufficiency/lifecycle, coding-standards artifacts, docs check and diff hygiene. It does not yet name T06 explicitly.

`EVALS.md` already states that T05 timeout left no treatment/reviewer comparison, T05B is packet-only, and no target/runtime/browser/CI/git/release/deploy/automation proof exists. It does not yet name a T06 decision result.

Both source registries already contain T05 and T05B entries. Neither registry has a T06 route marker yet.

The Track 11 plan has a `B45-POST-Q4-NEXT-TASKS` row that includes T06 as a promotion decision gate, plus T05/T05B evidence markers. It does not yet have a T06 completion marker.

`.codex/product-agent-os/lifecycle-state.json` currently points to `B45-POSTQ4-T05B-RERUN-PACKET-REVISION`, not T06. For a real T06 execution, the lifecycle marker must be refreshed after the visible Task Brief. For this review, marker mutation was out of scope.

## Compact Updates Needed For T06

Recommended source-owned artifact first:

- Create `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json`.
- Use evidence ID `B45-POSTQ4-T06-A01`.
- Decision state should be `keep_advisory_only_no_go_after_t05_timeout`.
- Record that static delta is useful local evidence but cannot promote.
- Record that T05 is inconclusive/no-go because treatment and reviewer evidence do not exist.
- Record that T05B remains `approval_required_not_run`.
- Preserve unsupported claims: no behavior improvement proof, no CI/blocker promotion, no runtime/browser/target/git/release/deploy/automation proof.

Recommended compact root/control-plane updates after that packet exists:

- `PLAN.md`: replace the current T05/T05B queue pointer with a one-line T06 status: `B45-POSTQ4-T06-A01 keeps advisory-only/no-go; T05B remains optional approval-required rerun`.
- `TEST.md`: add T06 to the existing Batch 45 post-Q4 route list, using the same focused checks; do not add a new broad suite.
- `EVALS.md`: add one sentence to the Batch 45 Q0-Q4/post-Q4 paragraph: T06 decision preserves no-go unless a later approved T05B rerun produces complete comparable evidence.
- `docs/sources/registry.md` and `docs/sources/registry.en.md`: add paired route markers for `B45-POSTQ4-T06-A01`.
- Track 11 plan: add one T06 row or marker near T05/T05B, and one compact historical marker.
- `.codex/product-agent-os/lifecycle-state.json`: refresh to T06 only during actual T06 execution, after the visible Task Brief.

## RUNLOG.md Routing

Do not add detailed T06 history to `RUNLOG.md`.

Current `RUNLOG.md` size observed in this review: `51123` bytes. The configured budget is `50 * 1024 = 51200` bytes, leaving only 77 bytes. Any normal T06 entry would push it over budget.

Use this routing instead:

- Detailed decision: `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json`.
- Discoverability: registry RU/EN markers.
- Sequencing: one compact `PLAN.md` pointer.
- Verification route: one compact `TEST.md` pointer.
- Claim ceiling: one compact `EVALS.md` sentence.
- Handoff state: if `RUNLOG.md` must change, use only a tiny pointer or mark `handoff_required_due_runlog_budget` in the T06 packet.

## Markers That Should Appear

Primary marker:

- `B45-POSTQ4-T06-A01`

Recommended status/decision markers:

- `keep_advisory_only_no_go_after_t05_timeout`
- `static_delta_not_promotion_evidence`
- `t05_inconclusive_no_treatment_no_reviewer`
- `t05b_approval_required_not_run`
- `m26_m27_m35_m37_boundaries_preserved`
- `ci_blocker_promotion_rejected_without_new_live_evidence`
- `runtime_browser_target_git_release_deploy_automation_not_proven`
- `runlog_handoff_required_due_budget`

Recommended packet path marker:

- `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json`

## Control-Plane Sync Decision

```yaml
control_plane_sync_decision:
  REQUIREMENTS.md: not_applicable_no_scope_or_acceptance_change_seen
  PLAN.md: update_required_compact_t06_status_pointer_after_packet
  TEST.md: update_required_compact_t06_route_pointer_after_packet
  EVALS.md: update_required_compact_t06_claim_ceiling_after_packet
  RUNLOG.md: handoff_required_due_runlog_budget
  prod_test.md: not_applicable_batch39_surface
  docs/sources/registry.md: update_required_t06_route_marker_after_packet
  docs/sources/registry.en.md: update_required_t06_route_marker_after_packet
  docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md: update_required_t06_marker_after_packet
  lifecycle_state: update_required_only_during_actual_t06_execution
```

## Verification

This review is inspection-only. No live/model/provider/runtime/browser/target/git actions were run.

Commands run:

- `rg` / `Get-Content` inspection of the requested files and supporting source packets.
- `Get-Item RUNLOG.md | Select-Object Name, Length`.
- `Get-ChildItem .codex/product-agent-os/reviews/batch45`.

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

## Residual Risks

- T06 is not source-complete until the decision packet exists.
- Root files are near their compactness limit; do not add narrative history to `RUNLOG.md`.
- If owner approves T05B later, T06 must not be treated as final promotion proof; it becomes the current no-go decision based on evidence available before that new run.

## Recommended Next Role

Product Manager or Release/Decision owner should create the T06 decision packet first, then Docs Maintainer can apply the compact registry/control-plane sync.
