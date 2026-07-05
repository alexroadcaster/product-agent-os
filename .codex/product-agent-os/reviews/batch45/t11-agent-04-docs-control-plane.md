# B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN: docs/control-plane analysis

Source status: project-local docs/control-plane review packet; inspection-only; no source, registry, test, root control-plane, runtime, provider, browser, target, git, release, deploy or automation action was performed.

## Scope

- Task: `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN`.
- Role: Docs Maintainer / docs-control-plane.
- Allowed write: this report only.
- Files read:
  - `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`
  - `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
  - `PLAN.md`
  - `TEST.md`
  - `EVALS.md`
  - `docs/sources/registry.md`
  - `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
  - `tests/product_agent_os/test_coding_standards_artifacts.py`
  - `.codex/config.toml`
  - `.codex/workflows/task-plan-lifecycle.md`
  - `.codex/workflows/control-plane-sync.md`

## Current source boundary

T11 is currently a planned optional next route, not implemented evidence:

- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json` routes T11 as `source_only_design` with status `optional_before_future_behavior_rerun`.
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json` contains T11 in `task_queue` and keeps the post-Q4 ceiling: T01-T03 prove copied-fixture static warning reduction only; T05 stopped on timeout; T06 keeps advisory-only/no-go; T08 records next routes.
- `PLAN.md`, `TEST.md`, `EVALS.md`, `docs/sources/registry.md`, and the Track 11 plan currently stop at post-Q4 T08 evidence and compact next-route pointers.
- `tests/product_agent_os/test_coding_standards_artifacts.py` already asserts the T08/T11 route exists, but does not yet assert a T11 design packet or T11 control-plane sync.

## Source-owned artifacts needed for T11

Primary source-owned artifact:

- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`

Recommended minimum fields:

- `schema_version`: `batch45_postq4_t11_treatment_v3_source_design_v1`
- `task_id`: `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN`
- `evidence_id`: `B45-POSTQ4-T11-A01`
- `status`: `implemented_source_only_treatment_v3_design_not_run`
- `source_status`: project-authored source-only design; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action
- `basis`: T08 packet, next-task packet, M26 result, T05 result, T06 decision, M35 decision, coding-standard source packets
- `problem_diagnosis`: why M26/treatment v2 likely added prompt friction or reviewer noise
- `design_principles`: smaller scaffold, planning/reviewer use, no generation-time prompt bloat, explicit negative examples, concrete behavior checks
- `treatment_v3_contract`: baseline/treatment separation, what changes, what does not change, allowed prompt/context surfaces
- `standards_to_behaviors_map`: coding standard -> expected agent behavior -> reviewer check -> failure mode
- `negative_examples`: custom-code overbuild, dependency addition without rationale, comment noise, missing existing-capability scan, unsupported readiness claims
- `future_eval_update_required`: T10 or future approval packet must update eval plan before any live run
- `control_plane_sync_decision`
- `no_unapproved_actions`
- `unsupported_claims`
- `verification`

Optional source-owned artifacts only if T11 uses multiple reviewers:

- `.codex/product-agent-os/reviews/batch45/t11-agent-01-treatment-design.md`
- `.codex/product-agent-os/reviews/batch45/t11-agent-02-eval-boundary.md`
- `.codex/product-agent-os/reviews/batch45/t11-agent-03-risk-review.md`

Do not create a public docs page for T11. This is internal source design, not user-facing product documentation.

## Exact files to update in the future T11 implementation

Source and queue:

- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`: add the source-only design packet.
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`: add `latest_t11_design`, include T11 in `executed_task_ids`, add `status_by_task["B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN"] = "implemented_source_only_treatment_v3_design_not_run"`, and preserve the no-go claim ceiling.

Registry:

- `docs/sources/registry.md`: add one compact RU registry marker for `B45-POSTQ4-T11-A01`.
- `docs/sources/registry.en.md`: add the matching compact EN registry marker for parity, even though only the RU registry was in the read list.

Root control-plane:

- `PLAN.md`: add or update one compact Batch 45 row/pointer for T11. Do not paste design details.
- `TEST.md`: extend the existing Batch 45 retest/post-Q4 command block to include `B45-POSTQ4-T11-A01` and the T11 packet path; keep the same focused commands unless T11 adds a new deterministic validator.
- `EVALS.md`: add one compact claim-ceiling marker: T11 is source-only design and does not reverse M26/M35/T05 or authorize a run.
- `RUNLOG.md`: do not add detailed T11 history. If a current-cycle pointer is mandatory, replace or shorten an existing Batch 45 current-route line instead of appending. Current size is `51123` bytes, only `77` bytes below the `50 * 1024` budget.
- `REQUIREMENTS.md`: `not_applicable` unless T11 changes scope, acceptance criteria, non-goals, or user-facing requirements.
- `prod_test.md`: `not_applicable`; Batch 39 surface.

Track 11 plan:

- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`: add a compact row after `B45-POSTQ4-T08` or update the Batch 45 current rows with `B45-POSTQ4-T11`; include packet path, source-only design status, verification gate, and stop conditions.

Tests:

- `tests/product_agent_os/test_coding_standards_artifacts.py`: add constants and assertions for the T11 packet and compact sync markers.

Lifecycle:

- `.codex/product-agent-os/lifecycle-state.json`: future implementation should update the lifecycle marker if the task runner allows it. This report did not update it because the user allowed writing only this report.

## Compactness risks

- `RUNLOG.md` is effectively full: current measured size is `51123` bytes against a `51200` byte budget. Any normal T11 entry will exceed the budget unless it replaces existing text.
- `PLAN.md` is `49697` bytes, `TEST.md` is `49908` bytes, and `EVALS.md` is `49908` bytes. They can accept only terse markers; detailed diagnosis, maps, negative examples and future eval design belong in the T11 JSON packet.
- T11 can easily duplicate T08/T10 content. Keep T08 as architecture routing history, T10 as live-eval harness redesign, and T11 as treatment source design only.
- Do not add a public docs page, new navigation, or root generated-site claim. T11 does not change user-facing docs.
- Do not turn source-only treatment design into readiness language. The allowed closure level is `docs_contract_ready` / source-only design, not behavior proof.

## Test assertions to add

Add a new test, for example `test_b45_postq4_t11_treatment_v3_source_design_is_source_only`, in `tests/product_agent_os/test_coding_standards_artifacts.py`.

Recommended assertions:

- `POST_Q4_T11_DESIGN = DOCS / "superpowers" / "specs" / "batch45-postq4-t11-treatment-v3-source-design.json"` exists and parses as JSON.
- Packet fields equal:
  - `schema_version == "batch45_postq4_t11_treatment_v3_source_design_v1"`
  - `task_id == "B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN"`
  - `evidence_id == "B45-POSTQ4-T11-A01"`
  - `status == "implemented_source_only_treatment_v3_design_not_run"`
- Packet route fields preserve:
  - `route == "source_only_design"`
  - no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action
  - `m26_reversed == false`
  - `m35_reversed == false`
  - `t05_timeout_reversed == false`
  - `future_eval_plan_update_required == true`
- Packet content contains:
  - diagnosis for M26/treatment underperformance
  - behavior map from standards to reviewer checks
  - negative examples
  - unsupported claims ledger
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json` records:
  - `latest_t11_design == "docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json"`
  - T11 in `execution_update.executed_task_ids`
  - status for T11 in `execution_update.status_by_task`
- `docs/sources/registry.md` and `docs/sources/registry.en.md` contain:
  - `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN`
  - `B45-POSTQ4-T11-A01`
  - `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`
  - wording that no live/model/runtime/browser/target/CI/git/release/deploy/automation proof exists
- `PLAN.md`, `TEST.md`, `EVALS.md`, and Track 11 plan contain compact `B45-POSTQ4-T11-A01` pointers.
- `RUNLOG.md` should not be required for test success unless the implementation intentionally replaces a compact current-cycle pointer; avoid asserting detailed RUNLOG text.
- Lifecycle marker assertion should be conditional or kept out of this focused test if the task write scope does not allow lifecycle marker updates.

Recommended command gate after implementation:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs only if T11 changes navigation, public docs, Markdown extensions, Mermaid, generated `site/`, search, sitemap or docs-tooling config. A source-only JSON packet plus compact root markers should not require a root site freshness claim.

## Unsupported claims to keep out

- `real_ai_agent_behavior_improvement`
- `M26_no_go_reversed`
- `M35_no_go_reversed`
- `T05_timeout_reversed`
- `treatment_v3_behavior_proven`
- `promotion_ready`
- `ci_workflow_readiness`
- `blocker_enforcement_readiness`
- `active_automation_readiness`
- `runtime_browser_readiness`
- `target_workspace_apply_safety`
- `provider_or_live_api_behavior`
- `release_deploy_publish_readiness`
- `root_site_freshness`
- `public_docs_readiness`
- `hook_activation_or_enforcement_changed`

## Control-plane sync decision for this report

- `REQUIREMENTS.md`: `not_applicable`.
- `PLAN.md`: `handoff_required`; future T11 implementation should add one compact pointer only.
- `TEST.md`: `handoff_required`; future T11 implementation should extend the Batch 45 post-Q4 check list with `B45-POSTQ4-T11-A01`.
- `EVALS.md`: `handoff_required`; future T11 implementation should add a compact source-only claim ceiling.
- `RUNLOG.md`: `handoff_required_due_runlog_budget`; do not append detailed history.
- `prod_test.md`: `not_applicable`.
- `docs/sources/registry.md`: `handoff_required`; add compact T11 source marker after source packet exists.
- `docs/sources/registry.en.md`: `handoff_required`; maintain parity.
- Track 11 plan: `handoff_required`; add compact row or marker for T11.

## Residual risks

- Exact T11 design schema is not yet implemented, so this report can only propose assertions.
- If T11 later changes eval semantics, T10/future live-eval packet must be updated before any run.
- Root files are near byte budget; any verbose sync should be rejected and moved into `docs/superpowers/specs/`.
- Lifecycle marker update is expected by workflow, but was not written in this slice because the user explicitly limited writes to this report.

