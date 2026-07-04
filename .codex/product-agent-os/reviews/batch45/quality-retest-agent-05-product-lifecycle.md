# Batch 45 Quality Retest Product/Lifecycle Report

Source status: `inspection-only product/lifecycle analysis`

Task ID: `B45-QUALITY-RETEST-PRODUCT-LIFECYCLE-A05`

## Scope

Question: what must a repeat test prove so that Professional Code Authoring / coding standards are accepted as actually applied and useful, not merely as a mechanism that reduces advisory warnings.

This report does not change code, tests, public docs, source registry, root control-plane files, target workspaces, hooks, CI, browser/runtime surfaces, provider calls, git state, release/deploy/publish state or automation. It writes only this review artifact.

## Sources Read

| Source | Product meaning |
| --- | --- |
| `docs/product-agent-os/coding-standards.md` | Defines Professional Code Authoring gates, activation surfaces, evidence ceiling and unsupported claims. |
| `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` | M26 live eval: warnings improved but behavior did not; promotion `no_go`. |
| `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json` | M27 owner decision: keep M25 local, non-blocking advisory only; no CI/blocker promotion. |
| `docs/superpowers/specs/batch45-real-project-scorecard.json` | M34 fixture-local scorecard: averages are not promotion gates; critical blockers override average. |
| `docs/superpowers/specs/batch45-real-project-decision-packet.json` | M35 decision: keep advisory-only/no-go; runtime/browser pilot requires fresh approval. |
| `docs/superpowers/specs/batch45-review-remediation-summary.json` | M37 remediation: local hook/validator hardening only; promotion state unchanged. |
| `PLAN.md` | Current sequencing: S6/S7/M37 are evidence-bound; M36 remains optional approval packet. |
| `RUNLOG.md` | Current handoff: Batch45 remains advisory-only/no-go; S7 is source-only without target/runtime proof. |

## Current Product Decision

Current state is `no_go_for_promotion_keep_advisory_only`.

The existing evidence proves that the advisory can reduce some warning output and can be locally hardened, but it does not prove that coding standards improve agent output quality in real tasks. The key negative signal is M26: treatment warnings fell from `29` to `15`, while average behavior score fell from `4.22` to `3.88`, treatment was worse on 4 of 8 tasks, one treatment run timed out, and the independent reviewer decision was `no_go`.

Therefore warning reduction is a proxy metric only. It can support reviewer ergonomics, but it cannot be the acceptance criterion for usefulness.

## Acceptance Criteria For A Meaningful Retest

Retest can support a stronger product claim only if it proves all of these:

| ID | Acceptance criterion | Evidence required | Owner |
| --- | --- | --- | --- |
| `B45-RT-AC01` | Standards are actually used before implementation decisions. | Per-task packet shows `enterprise_leverage_check`, `existing_capability_scan`, `one_line_candidate`, dependency decision, comment policy decision and unsupported-claim boundary before or during the coding work. | Product + reviewer |
| `B45-RT-AC02` | Standards improve behavior, not just warning count. | Treatment average beats baseline by a pre-declared margin and is not worse on a majority of tasks. Prior M26 threshold used `>= +0.5`; reuse it unless owner changes the threshold before running. | Product + independent reviewer |
| `B45-RT-AC03` | No critical regressions are hidden by averages. | Zero timeout/no-op/insufficient treatment runs for promotion; any critical behavior regression forces `no_go` even if aggregate score improves. | Tester + reviewer |
| `B45-RT-AC04` | Useful dimensions improve where standards claim value. | Improvement or non-regression in existing capability reuse, custom code avoidance, dependency avoidance, test scenario coverage, unsupported-claim discipline, reviewer usefulness, privacy safety and flake/cost control. | Reviewer |
| `B45-RT-AC05` | Runtime/product behavior is preserved for any real-project claim. | For selected disposable target or copied fixture, command/runtime/browser/API evidence proves the behavior acceptance scenario; static syntax/advisory evidence alone is insufficient. | Owner + tester |
| `B45-RT-AC06` | Warning reduction is interpreted correctly. | Advisory warnings are reported as input metric only, paired with counter-metrics: behavior score, task success, test/runtime proof, churn, reviewer judgment and false-positive/flake cost. | Product |
| `B45-RT-AC07` | Promotion surface is exactly matched to evidence. | Separate decision for local advisory, stronger advisory, CI, blocker enforcement, automation, target apply and public readiness; no promotion by implication. | Owner |

## Go / No-Go Thresholds

Use these thresholds before any stronger decision than advisory-only:

| Decision level | Minimum go threshold | Automatic no-go |
| --- | --- | --- |
| Keep local advisory | False positives controlled, output reviewer-sized, reversible disable path exists, no unsupported behavior claim. | Advisory blocks work, leaks paths/private data, or creates noisy output without reviewer value. |
| Claim standards improve agent behavior | Treatment average >= baseline + `0.5`, treatment better/equal on majority of tasks, zero critical treatment failures, independent reviewer `go`. | Treatment average <= baseline, treatment worse on majority, timeout/no-op/insufficient critical task, reviewer `no_go`. |
| Apply to real-project candidate | Static scorecard plus characterization/runtime evidence for the selected scenario and owner acceptance of target risk. | Only fixture/static/advisory evidence exists, or target behavior proof is missing. |
| Promote CI/blocker enforcement | Fresh behavior eval for exact enforcement surface, false-positive/flake replay, rollback/disable path, owner approval. | Current M27/M35 evidence remains unchanged, or no fresh approval. |
| Claim product readiness/release readiness | Runtime/browser/provider/database/security/rollback evidence for the exact product path. | Any of those surfaces are unsupported or approval-bound and not executed. |

## What Counts As Evidence That Standards Work

Valid evidence:

- Baseline vs treatment tasks are held out and comparable.
- Treatment output shows the standards changed decisions: smaller existing path, reuse/deletion/configuration, avoided dependency, clearer invariant comments, better tests or safer unsupported-claim boundary.
- Behavior score improves on product-relevant dimensions, not only on comment/advisory dimensions.
- The implementation still passes deterministic checks and any relevant runtime/manual acceptance scenario.
- Reviewer can explain what was rejected, why the chosen path is lower risk, and what remains unsupported.
- Privacy and data boundaries are preserved; no raw private traces or target source bodies are retained beyond approved/sanitized artifacts.
- Cost/flake/time stays acceptable and does not make the standard impractical.

Invalid or insufficient evidence:

- Warning count decreases while behavior score, tests, runtime proof or reviewer judgment regresses.
- Comment-only cleanup is scored as useful without proving behavior, safety or reviewer value.
- Static fixture scorecard is used to claim target behavior.
- A generated HTML/report/dashboard is treated as proof instead of orientation.
- One successful task is generalized to CI/blocker/automation promotion.
- Human review is replaced or bypassed by the standard.

## Recommended Retest Design

1. Pre-register the product question:
   `Does Professional Code Authoring improve agent implementation choices and acceptance evidence on held-out non-mechanical coding tasks?`
2. Select a balanced task set: include Python, JS/TS where relevant, docs/control-plane code, hook/validator work and at least one real-project-like scenario. Avoid reusing the exact manual pilot tasks as the only evidence.
3. Define two treatment arms: `baseline` without the coding-standard packet and `treatment` with the compact standards/checklist/handoff fields. Do not change more than one treatment variable.
4. Require per-task traceability: `requirement -> scenario -> code decision -> check/eval/manual QA -> evidence owner`.
5. Score dimensions separately: do not collapse into an average until critical blockers are evaluated. Runtime gap, privacy gap, unsupported claims, timeout/no-op and reviewer disagreement must override averages.
6. Add qualitative owner/reviewer review: owner decides whether the improvement is meaningful for real workflow cost and risk, not only numerically higher.
7. Decide promotion surface after evidence: local advisory, stronger advisory, CI, blocker enforcement, target apply, runtime/browser pilot and release claims are separate decisions.

## Decision Tree

```text
Start retest request
  |
  +-- Is the request only to reduce advisory warnings?
  |     -> Keep advisory-only. No behavior-improvement claim.
  |
  +-- Is there owner approval for provider/model eval if live agents are used?
  |     -> No: run source-only/static design or fixture scoring; claim ceiling stays docs_contract_ready/synthetic_green.
  |     -> Yes: run held-out baseline/treatment behavior eval.
  |
  +-- Did treatment beat baseline by the declared threshold and avoid critical regressions?
  |     -> No: no_go; keep advisory-only; record failure class.
  |     -> Yes: continue.
  |
  +-- Did reviewer/owner agree that improvements are product-meaningful?
  |     -> No: conditional_go for further design only.
  |     -> Yes: continue.
  |
  +-- Is runtime/target behavior proof needed for the claimed surface?
  |     -> Yes, but not approved/run: approval_required; no target/product readiness claim.
  |     -> Yes, approved and passed: eligible for target-specific conditional_go.
  |     -> No, static-only policy accepted: keep claim explicitly static-only.
  |
  +-- Is CI/blocker/automation promotion requested?
        -> Requires separate approval, exact promoted surface, rollback/disable path,
           false-positive/flake/cost replay and fresh behavior eval for that surface.
```

## User Approvals Needed

Fresh exact approval is needed for:

- provider/model/API calls for live behavior eval reruns;
- browser automation, runtime launch or target command execution;
- target workspace mutation, disposable clone mutation or target fixture creation outside already approved source policy;
- database or production/local private data access;
- CI workflow creation, blocker enforcement, stronger hook/advisory promotion or hook activation beyond current local non-blocking advisory;
- git stage/commit/push/branch/PR;
- release, deploy, publish, package/cache refresh or external write;
- active automation, schedules, recurring jobs or Self-Learning Loop auto-apply.

Owner also needs to decide before retest:

- task set and target labels;
- threshold delta, default recommendation `>= +0.5` over baseline;
- whether TypeScript/JS advisory coverage is in scope;
- whether runtime/browser proof is required now or accepted as a gap for a static-only decision;
- whether the desired output is advisory-only confidence, treatment v2 design, real-project pilot, or promotion packet.

## Product Risks

- Proxy metric risk: warning reduction can reward comment-only or suppression-oriented edits.
- Churn risk: checklist-guided treatment can create larger refactors before characterization/runtime proof exists.
- Language coverage risk: current local advisory hardening improves TS/TSX scanning, but prior SOL evidence still recorded TypeScript coverage gaps.
- Evaluation cost/flake risk: M26 included one timeout and high elapsed time; future eval must budget time and failure handling.
- Claim creep risk: M34/M35/M37 are source/static/local-hardening evidence and do not reverse M26/M27 no-go.
- Owner calibration risk: score weights need owner/reviewer agreement before a future promotion packet.

## Recommended Current Decision

Current decision should remain:

`keep_advisory_only_no_go_for_promotion`.

Recommended next route depends on owner intent:

| Owner intent | Next role | Next action |
| --- | --- | --- |
| Understand evidence only | Product manager | Use this report as the retest acceptance boundary. |
| Design a better treatment v2 | Product manager + tester | Produce source-only retest protocol and scoring rubric; no live/provider/target action. |
| Prove behavior with live agents | Tester/eval designer | Request provider/model approval and run held-out baseline/treatment eval. |
| Prove target/runtime behavior | Runtime/browser pilot planner | Prepare `B45-PCA-M36` approval packet with target, commands, rollback, data boundary and evidence artifacts. |
| Promote CI/blocker/automation | Release/operator + reviewer | Stop until fresh behavior eval, false-positive/flake replay and explicit promotion approval exist. |

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this report does not change project scope or acceptance source of truth.
- `PLAN.md`: `not_applicable`; sequencing is analyzed but not changed.
- `TEST.md`: `not_applicable`; no verification route is changed.
- `EVALS.md`: `not_applicable`; retest thresholds are recommended here only, not promoted into source truth.
- `RUNLOG.md`: `handoff_not_written`; detailed analysis belongs in this requested review artifact and RUNLOG is near budget.
- `prod_test.md`: `not_applicable`; Batch 39 surface unaffected.
- Source registry: `not_applicable`; this is an internal review artifact, not a new public source-backed claim.

## Handoff

Product decision: keep advisory-only/no-go until a fresh retest proves behavior improvement with no critical regressions and owner-reviewed product usefulness.

Acceptance behavior: warning reduction is only an input signal; go requires baseline/treatment behavior improvement, reviewer usefulness, traceability, deterministic checks and runtime/target evidence where the claim needs it.

Non-goals: no code changes, no hook/CI/blocker promotion, no target apply, no runtime/browser/provider execution, no release/readiness claim.

Assumptions: owner wants a product/lifecycle decision framework, not immediate retest execution.

Risks: proxy metric misuse, score averaging over critical blockers, unapproved live/provider/target surfaces, owner calibration gap.

Verification expectation: this report is inspection-only. Any future promotion requires current-run evidence for the exact promoted surface.

Recommended next role: `tester/eval designer` for a retest protocol, or `runtime/browser pilot planner` only if owner explicitly chooses `B45-PCA-M36`.
