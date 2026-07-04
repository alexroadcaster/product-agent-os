# Batch 45 Quality Retest - Completion Skeptic

Source status: independent evidence-gate review artifact.

Task ID: `B45-QUALITY-RETEST-COMPLETION-SKEPTIC-A06`
Review date: 2026-07-04
Role: completion-skeptic / independent evidence gate
Mode: local source review plus focused local checks; no code changes, no external/runtime/provider/browser/target/git/release/automation actions.

## Scope

Question: is the workspace ready to launch repeat code-quality/refactoring testing after `B45-PCA-M37-A01`, and what claims/gaps/tests can mislead the next retest decision?

This review writes only this artifact. It does not repair implementation, change tests, alter public docs, mutate target workspaces, activate hooks, run providers, launch browsers, run live servers, use git actions, publish, deploy or enable automation.

## Sources Read

- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md`
- `.codex/product-agent-os/reviews/batch45/remediation-agent-03-final-review.md`
- `.codex/product-agent-os/reviews/batch45/remediation-agent-04-code-repair.md`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- `EVALS.md`
- `TEST.md`
- `.codex/product-agent-os/lifecycle-state.json`
- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- Existing quality-retest handoffs: `quality-retest-agent-02-runtime-validator.md`, `quality-retest-agent-04-security-privacy-approval.md`, `quality-retest-agent-05-product-lifecycle.md`.

Memory was used only as recall for Batch 45 context; current files and current command output override memory.

## Executive Recommendation

Recommendation: `no_go_for_unqualified_retest_launch`.

Current evidence does not support launching a broad repeat code-quality/refactoring retest if the expected output is behavior-improvement, promotion, CI/blocker, target/runtime/browser/provider, release, deploy, automation or product-readiness evidence.

Narrow exception: `conditional_go_for_local_static_advisory_retest_only` after a retest packet is written. That packet must name corpus, arms, thresholds, approval boundary, evidence artifacts, privacy boundary, false-positive handling and stop conditions. The allowed retest ceiling is `local_advisory_static_retest_with_gaps`, not promotion.

## Claim Ledger

### Supported Claims

- `B45-PCA-M37-A01` supports local non-blocking advisory hardening only: TS/TSX scanning, fail-open hook diagnostics, path redaction, active/template hook parity and docs/control-plane/source sync.
- Current-run focused hook/validator checks passed: `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v` ran 26 tests with `OK`.
- Current-run M37 docs/control-plane check passed after the lifecycle marker was restored to the owner M37 state: `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v` ran 11 tests with `OK`.
- Current-run docs structure check passed: `python tools\check_docs.py` returned `OK: documentation structure checks passed`.
- Current-run scoped diff hygiene passed: `git diff --check -- <M37 scoped write set>` exited `0`; Git reported CRLF-to-LF working-copy warnings on changed markdown/control-plane files.
- M26 remains negative behavior evidence: baseline average `4.22`, treatment average `3.88`, warnings `29 -> 15`, 15/16 completed, one timeout, independent reviewer `no_go`.
- M35 remains a no-go decision packet: keep advisory-only, no CI/blocker promotion, no target apply, no runtime/browser/provider/database/git/release/deploy/publish/automation claim.

### Unsupported Claims

- Ready to launch broad repeat quality/refactor testing without a pre-registered retest packet.
- Real AI-agent behavior improvement after M37.
- Treatment v2 promotion readiness.
- CI/blocker enforcement readiness.
- Target workspace safety after mutation.
- Runtime/browser/provider/database behavior.
- Release/deploy/publish/product-readiness.
- Automation or hook activation readiness.
- TS/TSX parser completeness.
- Broad false-positive or false-negative rate.
- Clean-tree or large-change hook output as sufficient retest coverage.
- Warning reduction as proof of better code quality.

### Contradicted Claims

- Claim: "warning count reduction proves standards work." Contradicted by M26: warnings fell while behavior score also fell and reviewer decision stayed `no_go`.
- Claim: "M37 reverses M35 no-go." Contradicted by M37 summary and M35 decision packet: M37 is local hardening/docs sync only and leaves promotion `no_go/advisory-only`.
- Claim: "focused M37 tests prove retest readiness." Contradicted by `TEST.md` and existing quality-retest reviews: those tests prove local hook/docs contracts, not broad behavior, target runtime, parser completeness or owner usefulness.
- Claim: "`remediation-agent-03-final-review.md` no-go is fully current." Partially contradicted by current `remediation-agent-04-code-repair.md` and current test output: the missing artifact and code-side fail-open/path items appear repaired. The broader no-go for promotion/retest claims remains current.

## Must-Close Gaps Before Retest

### Blockers For Any Meaningful Retest Launch

1. `retest_packet_missing`: no current source-owned retest packet names the exact retest objective, corpus, tasks, treatment arms, metrics, thresholds, owner/reviewer, evidence paths and stop conditions.
2. `acceptance_threshold_missing`: the retest has not predeclared whether it is testing advisory noise, behavior improvement, treatment v2 design, target preservation or promotion. These are different gates.
3. `corpus_scope_missing`: no approved list of files/tasks/fixtures exists for the repeat quality/refactor retest. Hook-only changed-file scanning is insufficient.
4. `baseline_treatment_design_missing`: no current baseline/treatment protocol prevents the next run from changing multiple variables at once.
5. `false_positive_plan_missing`: no retest-specific plan explains how advisory warnings, self-noise, suppression behavior and parser blind spots will be scored.
6. `privacy_boundary_missing_for_new_artifacts`: any fixture refresh or target evidence needs explicit allowed file classes, redaction manifest, denylist handling, no raw source/log/private data retention and deletion path.
7. `approval_boundary_missing_for_nonlocal_surfaces`: runtime/browser/provider/live eval/target command/target mutation/git/release/deploy/automation surfaces remain blocked until an M36-style approval packet exists.

### Blockers For Stronger Than Local Static Claims

- `provider_or_live_eval_required`: behavior-improvement claims need fresh approved live baseline/treatment eval; current M26 evidence is negative.
- `runtime_browser_required`: real-project behavior preservation needs approved disposable runtime/browser proof; M36 is reserved but not executed.
- `owner_reviewer_calibration_required`: score weights and critical-regression rules need owner/reviewer agreement before promotion.
- `critical_failure_policy_required`: timeout, no-op, insufficient evidence and target-read-only failure must override averages.
- `promotion_surface_required`: local advisory, stronger advisory, CI, blocker, target apply, automation and public readiness must each have separate approval and evidence.

## Insufficient Tests

Current M37 tests are necessary but not sufficient.

- `test_comment_sufficiency` and `test_lifecycle_hooks` prove focused validator/hook behavior, not broad code-quality improvement.
- `test_coding_standards_artifacts` proves source links and claim ceilings, not retest effectiveness.
- `tools\check_docs.py` proves documentation structure only.
- `git diff --check` proves whitespace hygiene only.
- M26 live eval is stale for post-M37 behavior and negative for promotion.
- M34/M35 real-project evidence is fixture-local/static/no-go and cannot prove runtime or target behavior.

Missing test/evidence classes before retest:

- explicit broad corpus CLI run with caps disabled: `--include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1`;
- clean-tree hook and `>20` changed-files skip classified as non-coverage, not success;
- TS/TSX typed const assignment, multiline signatures, class field arrows, object-property methods and exported wrapper forms;
- JS brace counting with strings/comments/template literals;
- unrelated preceding comments that should not suppress warnings;
- nested Python functions and `run_*` exception behavior;
- CLI syntax-error behavior over broad corpus;
- redaction matrix beyond root and `USERPROFILE`;
- per-task reviewer scoring that separates warning count from behavioral quality.

## False-Positive / False-Confidence Risks

- `warning_proxy_risk`: warning reduction can reward comment-only or suppression-oriented changes while behavior regresses.
- `hook_noncoverage_risk`: a clean tree, skipped large diff or wrong changed-file set can look like an advisory success.
- `summary_packet_risk`: generated/source-owned summaries can repeat earlier evidence but do not prove new retest readiness by themselves.
- `score_average_risk`: averages can hide timeout, no-op, insufficient evidence, target-read-only failure or runtime gap.
- `static_fixture_risk`: fixture-local/static scorecards can look like real-project proof while target runtime remains untested.
- `parser_blind_spot_risk`: regex TS/TSX parsing can miss common forms and still produce green focused tests.
- `lifecycle_marker_false_red_risk`: current M37 docs test expects `.codex/product-agent-os/lifecycle-state.json` task_id `B45-PCA-M37-A01`; a parallel review marker can cause a red test unrelated to M37 code quality. I observed this transiently and restored the owner M37 marker before final evidence.
- `CRLF_warning_risk`: scoped `git diff --check` exits `0`, but CRLF-to-LF warnings on changed markdown/control-plane files can create noisy future diffs.

## Go / No-Go Matrix

| Retest target | Decision | Reason |
| --- | --- | --- |
| Local advisory smoke over current changed files | `conditional_go` | M37 focused tests are green, but hook output is changed-file scoped and not broad coverage. |
| Explicit local static corpus retest | `conditional_go_after_packet` | Needs corpus, CLI command, thresholds, privacy boundary, false-positive policy and owner/reviewer scoring. |
| Repeat live behavior eval | `no_go_until_approval` | Provider/model/live eval approval and baseline/treatment protocol required; M26 is negative. |
| Disposable runtime/browser pilot | `no_go_until_M36_packet` | M35 reserves M36; target, commands, rollback, data boundary and evidence artifacts are required. |
| CI/blocker promotion | `no_go` | M27/M35 reject promotion; no fresh behavior/flake/false-positive evidence for exact promoted surface. |
| Target apply / product readiness / release readiness | `no_go` | Runtime/browser/provider/database/security/rollback/release evidence is absent or approval-bound. |

## Smallest Evidence Path

1. Write a source-owned retest packet, for example `docs/superpowers/specs/batch45-quality-retest-protocol.json`.
2. Declare one objective: advisory-noise audit, treatment v2 source design, live behavior eval, or runtime/browser pilot. Do not mix them.
3. For local-only retest, run explicit corpus CLI, not hook-only:

```powershell
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py <approved-corpus-paths> --root . --include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1
python .codex\hooks\comment_sufficiency_advisory.py
```

4. Re-run the M37 focused checks:

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python tools\check_docs.py
git diff --check -- .codex/hooks/comment_sufficiency_advisory.py .codex/product-agent-os/lifecycle-state.json docs/product-agent-os/coding-standards.md docs/product-agent-os/coding-standards.en.md docs/sources/registry.md docs/sources/registry.en.md docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md PLAN.md EVALS.md TEST.md docs/superpowers/specs/batch45-review-remediation-summary.json plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py tests/product_agent_os/test_comment_sufficiency.py tests/product_agent_os/test_lifecycle_hooks.py tests/product_agent_os/test_coding_standards_artifacts.py
```

5. If the intended claim is behavior improvement, request approval for fresh live baseline/treatment eval and predeclare thresholds: treatment average >= baseline + `0.5`, not worse on majority, zero critical failures, independent reviewer `go`.
6. If the intended claim is target/runtime behavior, create the `B45-PCA-M36` approval packet before any target command, runtime launch or browser automation.

## Current Commands Run

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
```

Result: exit `0`; 26 tests; `OK`.

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
```

Result after restoring the owner M37 lifecycle marker: exit `0`; 11 tests; `OK`.

```powershell
python tools\check_docs.py
```

Result: exit `0`; `OK: documentation structure checks passed`.

```powershell
git diff --check -- <M37 scoped write set>
```

Result: exit `0`; no whitespace errors; CRLF-to-LF warnings reported for changed markdown/control-plane files.

No broad corpus retest, live eval, browser/runtime proof, provider call, target command, target mutation, git action, release/deploy/publish or automation was run.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this review does not change scope or acceptance source of truth.
- `PLAN.md`: `handoff_required_if_owner_selects_retest`; current plan already keeps M37 advisory-only/no-go. Add sequencing only when a concrete retest protocol is selected.
- `TEST.md`: `handoff_required_if_retest_scheduled`; recommended retest commands belong in a future retest protocol unless owner schedules the retest now.
- `EVALS.md`: `not_applicable`; current claim ceilings already reject unsupported runtime/product/release claims.
- `RUNLOG.md`: `handoff_required_not_updated`; root RUNLOG is near budget and this detailed evidence belongs in the requested source-owned review artifact.
- `prod_test.md`: `not_applicable`; Batch 39 surface unaffected.
- Source registry: `not_applicable`; this internal skeptic review does not create a public source-backed claim.

## Blocker Checklist

- [ ] Retest objective selected and written in a source-owned packet.
- [ ] Corpus/task list approved and privacy-safe.
- [ ] Baseline/treatment design predeclared.
- [ ] Thresholds and critical failure overrides predeclared.
- [ ] Reviewer/owner scoring responsibilities assigned.
- [ ] Broad corpus CLI command selected; hook-only evidence rejected as insufficient.
- [ ] False-positive/false-negative classes either tested or accepted as explicit gaps.
- [ ] Runtime/browser/provider/target/git/release/deploy/automation boundaries recorded.
- [ ] M36 approval packet created before any runtime/browser/target proof.
- [ ] M37 focused checks rerun in the same current run as the retest launch.
- [ ] Unsupported claim list copied into the retest output template.

## Next Recommended Role

Recommended next role: `Eval/Test Engineer` to write a source-owned local-only retest protocol.

Do not route to `Release Operator`. Route to runtime/browser pilot planner only if the owner explicitly requests `B45-PCA-M36` with exact target, commands/actions, rollback/delete path, data/privacy boundary and evidence artifacts.
