# Batch 45 Remediation Agent 02 - Docs / Control-Plane

Source status: project-authored remediation handoff.

## Scope

Implemented `B45-PCA-M37` / `B45-PCA-M37-A01` as a source-owned Batch 45 review remediation packet for local advisory hardening and docs/control-plane/source sync only.

This slice did not occupy `B45-PCA-M36`; M36 remains reserved for an optional runtime/browser approval packet.

## Files Changed

- `.codex/product-agent-os/lifecycle-state.json`
- `docs/product-agent-os/coding-standards.md`
- `docs/product-agent-os/coding-standards.en.md`
- `docs/sources/registry.md`
- `docs/sources/registry.en.md`
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`
- `PLAN.md`
- `EVALS.md`
- `TEST.md`
- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `tests/product_agent_os/test_coding_standards_artifacts.py`
- `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md`

`RUNLOG.md` was not changed: observed size was 51,123 bytes against the 51,200-byte workflow budget, so detailed handoff was routed here and to the summary packet as `handoff_required_due_runlog_budget`.

## Source Evidence

- `agent-01-architecture-lifecycle.md`: lifecycle marker was stale at M27; control-plane sync vocabulary needed final-state clarity.
- `agent-03-verification-evals.md`: M26 15/16 live eval is negative/no-go evidence, not partial success; promotion needs fresh approval-gated evidence.
- `agent-04-docs-source-sync.md`: public RU/EN page was conservative but stale relative to S6/S7; RUNLOG was near budget.
- `agent-06-product-scenarios-scorecard.md`: scorecard supports blocking promotion; static averages must not be read as readiness.
- M26/M27/M35 source packets remain the evidence ceiling for no-go/advisory-only status.

## What Changed

- Added `docs/superpowers/specs/batch45-review-remediation-summary.json` with M37 scope, no-unapproved-actions proof, unsupported claims, control-plane sync decision and verification results.
- Updated lifecycle marker to `B45-PCA-M37-A01` with `local_synthetic_hardening_no_promotion_claim`.
- Updated RU/EN public coding standards to name M26/M27/M35/M37 and reject unsupported runtime/browser/provider/target/git/release/deploy/automation claims.
- Added RU/EN source registry M37 routes and detailed marker.
- Added compact M37 pointers to Track 11, `PLAN.md`, `EVALS.md` and `TEST.md`.
- Added a focused test for M37 packet and public docs/source registry/control-plane linkage.

## Commands And Results

- `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`
  - Result: exit 0, 11 tests OK.
- `python tools\check_docs.py`
  - Result: exit 0, `OK: documentation structure checks passed`.
- `git diff --check -- .codex/product-agent-os/lifecycle-state.json docs/product-agent-os/coding-standards.md docs/product-agent-os/coding-standards.en.md docs/sources/registry.md docs/sources/registry.en.md docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md PLAN.md EVALS.md TEST.md RUNLOG.md docs/superpowers/specs/batch45-review-remediation-summary.json tests/product_agent_os/test_coding_standards_artifacts.py`
  - Result: exit 0; no whitespace errors. Git reported CRLF-to-LF working-copy warnings for changed Markdown files.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable_no_scope_or_acceptance_change`
- `PLAN.md`: `updated_compact_pointer`
- `TEST.md`: `updated_focused_check_route`
- `EVALS.md`: `updated_claim_ceiling_and_eval_route`
- `RUNLOG.md`: `handoff_required_due_runlog_budget`
- `prod_test.md`: `not_applicable_batch39_surface`
- `docs/sources/registry.md`: `updated_source_route`
- `docs/sources/registry.en.md`: `updated_source_route`
- `.codex/product-agent-os/lifecycle-state.json`: `updated_current_marker`

## Unsupported Claims Kept Out

- Real AI-agent behavior improvement.
- Target/runtime/browser/provider/database behavior.
- Target mutation safety.
- CI/blocker promotion.
- Git/release/deploy/publish readiness.
- Active automation readiness.

## Residual Risks

- `RUNLOG.md` remains near budget and should not receive detailed Batch 45 history without compaction.
- `B45-PCA-M36` is still optional and not executed.
- Hook/code/comment-sufficiency remediation is explicitly outside this slice and belongs to another agent.
- Promotion remains `no_go/advisory-only`; M26 live eval and S7 fixture-local evidence do not support promotion.

## Recommended Next Role

Owner or runtime/browser pilot planner only if `B45-PCA-M36` is explicitly requested with exact target, commands, rollback, browser/provider/git/external boundaries and evidence requirements. Otherwise keep Professional Code Authoring advisory-only.
