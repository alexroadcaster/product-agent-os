# B45-POSTQ4-T10 Completion Skeptic Sidecar

Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`

Role: `completion-skeptic`

Created: `2026-07-05`

Scope: sidecar review for the future T10 live-eval harness redesign packet. This report is claim/evidence review only. It does not run or approve live/model/provider/runtime/browser/target/git/CI/automation actions.

## Source Ledger

Current source files read:

- `.codex/config.toml`: lifecycle and control-plane workflows are config-routed through `[product_agent_os.lifecycle_contract]` and `[workflows]`.
- `.codex/workflows/task-plan-lifecycle.md`: requires visible Task Brief before execution and Completion Brief after execution or handoff.
- `.codex/workflows/control-plane-sync.md`: requires a control-plane sync decision before closing Product-Agent OS work.
- `.codex/product-agent-os/lifecycle-state.json`: current marker still belongs to `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN`; this T10 sidecar did not update it because the owner limited writes to exactly this report file.
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`: M26 live held-out eval.
- `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`: T05 approved rerun timeout rollup.
- `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`: T05B revised approval packet.
- `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json`: post-Q4 promotion/no-go decision.
- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`: T08 architecture next-actions.
- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`: T11 source-only treatment v3 design.
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`: post-Q4 queue and T10 acceptance.
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`: M35 no-go decision boundary.
- `tests/product_agent_os/test_coding_standards_artifacts.py`: current assertions around post-Q4 packet routes and claim ceilings.
- `PLAN.md`, `TEST.md`, `EVALS.md`, Track 11 plan and source registry entries were read through targeted search/context only; no edits were made.

Generated `site/`, previous reports and memory were treated as orientation only, not source proof.

## Claim Ceiling

T10 can claim only this, after its source packet exists and passes the required checks:

- A source-owned live-eval harness redesign packet was created for review.
- The packet separates evidence classes: static warning delta, live/model behavior, runtime/browser proof, governance/promotion.
- The packet redesigns future approval/run policy so timeouts do not erase comparability by accident.
- The packet names approval-required surfaces, temp-only raw retention, cost/call caps, reviewer timing, abort conditions and no-unapproved-actions proof.
- The packet can be `docs_contract_ready` or `approval_packet_only`, not behavior-proven.

T10 cannot claim:

- Real AI-agent behavior improvement.
- Treatment v3 behavior improvement.
- M26, M27, M35, T05 or T06 reversal.
- Provider/model/live rerun permission.
- Runtime/browser/target behavior or product acceptance.
- CI workflow readiness, blocker enforcement, active automation, release/deploy/publish readiness.
- That static warning delta `14 -> 0` proves behavior quality.
- That T05B approval exists; T05B is a packet and still requires new exact owner approval before any rerun.

## Supported Claims

- M26 is a live-eval no-go: baseline average `4.22`, treatment average `3.88`, treatment worse on 4 of 8 tasks, one timeout, reviewer `no_go`.
- T05 is inconclusive/no-go: one baseline run completed, the second baseline run timed out, treatment and reviewer did not run, remaining calls stopped by policy.
- T05B is approval-packet-only and cannot reuse the consumed T05 approval.
- T06 keeps M25 advisory-only and rejects stronger advisory, CI, blocker and automation promotion from current evidence.
- T08 correctly routes T10 before any new T05B behavior rerun when the owner wants better live-eval evidence.
- T11 is source-only treatment v3 design and explicitly requires T10 before any approved rerun.
- Current post-Q4 evidence supports local/static maintenance improvement only; no runtime/browser/target/CI/git/release/deploy/automation proof exists.

## Unsupported Or Contradicted Claims

Unsupported:

- T10 is complete now. No T10 source packet was present in the source files read.
- T10 can approve a rerun by itself. It can only stage the approval contract.
- T05B is runnable without fresh owner approval.
- A future rerun can count timeout, no-op or null-score pairs as behavior success.
- Warning-count reduction can substitute for behavior score or reviewer decision.
- A reviewer can run after an invalid primary comparison and still produce promotion evidence.

Contradicted by current sources:

- `M26_no_go_reversed`: contradicted by M26, T05, T06, T08 and T11.
- `T05_timeout_reversed`: contradicted by T05 and T06.
- `M35_no_go_reversed`: contradicted by M35, T06 and T11.
- `promotion_allowed`: contradicted by T06 decision and next-task claim ceiling.

## Blockers Before Any Future Live/Model Rerun

Hard blockers:

- New exact owner approval is missing for any T05B/T10-derived live/model/provider call.
- T10 source packet is not yet present as an owning source artifact.
- The future harness must pick one explicit timeout policy before execution: strict stop, paired continue, retry-on-timeout, or diagnostic-only.
- The future harness must define paired baseline/treatment ordering before any run.
- The future harness must define which pairs are valid, invalid, timeout, no-op or null-score and forbid invalid pairs from promotion math.
- Reviewer timing must be explicit: reviewer runs only after primary evidence is comparable under the chosen policy.
- Cost cap must be exact or explicitly accepted as `cost_unavailable_call_count_cap_only`.
- Process watchdog must include outer timeout, process-tree kill, timeout marker and lingering-process check.
- Retention must remain raw-temp-only; repo may store only sanitized rollups, hashes and metadata.
- Disposable temp root, source freeze and cleanup safety must be proven before model calls.

Approval blockers:

- Provider/model/surface must be restated by the owner.
- Run count must be restated by the owner, including setup/smoke calls if any.
- Any runtime/browser/target proof must route separately through T07/B45-PCA-M36-style approval, not T10.
- Any target workspace command, mutation, database access, CI/blocker creation, git, release, deploy, publish or automation action needs separate exact approval.

## Promotion Blockers

Promotion remains blocked until a future approved run proves all of these:

- Comparable baseline/treatment evidence exists for enough valid pairs.
- Treatment quality improves by the packet threshold, not just warning count.
- Treatment is equal or better on the required pairwise threshold.
- Timeout/no-op/null-score pairs are quarantined and do not help promotion.
- Independent reviewer decision is not `no_go`.
- Runtime/browser/target claims, if made, have separate activation/fallback proof.
- CI/blocker/automation rollout has rollback, false-positive, flake and owner-risk evidence.

Current evidence blocks promotion because:

- M26 treatment underperformed baseline.
- T05 produced no treatment arm and no reviewer comparison.
- T05B did not run.
- T06 already rejected stronger advisory, CI, blocker and automation promotion.
- T11 is only source design.

## Required Verification Before Saying T10 Source Packet Is Complete

T10 source packet can be called complete only after current-run evidence proves all required source-contract items:

- A source packet exists at an agreed source-owned path, likely under `docs/superpowers/specs/`.
- The packet references M26, T05, T05B, T06, T08, T11, M35 and `batch45-post-q4-next-tasks.json`.
- The packet includes claim ceiling and unsupported claims.
- The packet separates strict stop-on-timeout, paired continue, retry-on-timeout and diagnostic-only routes.
- The packet defines per-task pairing, timeout budget, reviewer timing, cost cap handling, temp-only raw retention and abort conditions.
- The packet defines valid/invalid pair math and promotion thresholds.
- The packet contains no-unapproved-actions proof for T10 packet creation.
- The packet records exact approval fields that remain owner-fill-required before future execution.
- The packet is covered by focused assertions in `tests/product_agent_os/test_coding_standards_artifacts.py` or an equivalent current test.
- Source registry RU/EN and compact control-plane pointers are updated by the owning docs/control-plane role, unless an explicit handoff is recorded.
- JSON/Markdown syntax and docs checks run in the current completion run.
- `git diff --check` runs and shows no whitespace errors.

Minimum verification command set for the owner/source-packet implementer:

- `python -m json.tool <T10-source-packet.json>` if the packet is JSON.
- `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`
- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `git diff --check`

This sidecar itself did not run those checks after writing because the owner requested exactly one report file and no broader source-packet implementation exists in this slice.

## Failure Modes To Guard

- Treating T10 as approval instead of approval-packet redesign.
- Reusing T05 approval after it was consumed.
- Running model calls while writing the packet.
- Letting one early timeout destroy both treatment comparability and reviewer usefulness again.
- Counting partial, no-op or null-score outputs as success.
- Allowing static warning deltas to dominate behavior scoring.
- Running reviewer on non-comparable primary evidence and presenting it as promotion-grade.
- Retaining raw prompts, raw model traces, private source bodies or provider payloads in repo.
- Forgetting process-tree cleanup and leaving scoped provider/model wrappers running.
- Mixing T10 behavior-eval proof with T07 runtime/browser proof.
- Updating root `RUNLOG.md` with detailed history instead of source-owned packet pointers.
- Omitting registry/control-plane sync after the source packet is implemented.
- Claiming source packet complete without tests that assert the no-run/no-promotion boundary.

## Accepted Gaps For This Sidecar

- Lifecycle marker was not updated for T10 because the owner explicitly constrained writes to exactly one report file. The visible Task Brief was shown in chat.
- No T10 source packet exists in this sidecar; this file is a completion-skeptic review artifact only.
- No live/model/provider/runtime/browser/target/git/CI/automation check was run by design.
- No docs/control-plane files were edited; control-plane decisions are recorded below as handoff-required/not-applicable.

These gaps are accepted only for creating this sidecar report. They are not accepted for saying T10 source packet is complete.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this sidecar did not change user scope or acceptance criteria.
- `PLAN.md`: `handoff_required`; T10 source-packet implementer/docs-control-plane owner should add a compact pointer only after the actual T10 source packet exists.
- `TEST.md`: `handoff_required`; add verification commands/assertions only with the actual T10 packet.
- `EVALS.md`: `handoff_required`; add or confirm T10 claim ceiling only with the actual T10 packet.
- `RUNLOG.md`: `handoff_required_due_runlog_budget`; do not expand detailed Batch 45 history in root runlog.
- `prod_test.md`: `not_applicable`; Batch 39 surface.
- `docs/sources/registry.md`: `handoff_required`; source route should be added only for the actual T10 source packet, not this sidecar alone unless project policy wants review artifacts registered.
- `docs/sources/registry.en.md`: `handoff_required`; same as RU registry.
- `.codex/product-agent-os/lifecycle-state.json`: `handoff_required`; not edited due exact-one-file constraint.

RUNLOG overflow decision: do not edit or expand `RUNLOG.md` in this sidecar.

Files updated: `.codex/product-agent-os/reviews/batch45/t10-agent-05-completion-skeptic.md` only.

## Exact Blocker

The exact blocker before any future live/model rerun is missing new exact owner approval plus missing implemented T10 harness source packet with timeout/pairing/reviewer/cost/retention/no-unapproved-actions contract.

The exact blocker before a T10 source-packet completion claim is simpler: the T10 source packet and its focused verification evidence do not exist in this slice.

## Smallest Next Action

Recommended smallest next action: Builder or Docs Maintainer creates the T10 source-owned packet only, with no model/provider/runtime/browser/target/git/CI/automation actions, then Tester adds focused assertions and runs the current docs/test/diff checks.

Recommended next role: Docs Maintainer for source-packet/control-plane alignment, then Tester for assertions, then Completion Skeptic for final claim gate.

## Completion Brief

- Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- Result status: `sidecar_report_created_source_review_only_not_T10_packet_complete`
- What was done: read current lifecycle/control-plane workflow, M26/T05/T05B/T06/T08/T11/M35/post-Q4 queue sources and wrote a completion-skeptic sidecar defining supported claims, unsupported claims, blockers, promotion blockers, required verification and failure modes.
- Files / artifacts changed: `.codex/product-agent-os/reviews/batch45/t10-agent-05-completion-skeptic.md`
- Verification evidence: source read audit plus one-file report creation. No live/model/provider/runtime/browser/target/git/CI/automation action was performed. Post-write broader verification is a gap because this slice was constrained to exactly one report file and did not implement the T10 source packet.
- Residual risks / accepted gaps: lifecycle marker and root control-plane files were not updated due exact-one-file constraint; T10 source packet remains missing; no completion/readiness/promotion claim is supported.
- Follow-up: implement T10 source packet, add focused assertions, run docs/test/diff checks, then reroute to completion-skeptic before any future approval-gated rerun.
