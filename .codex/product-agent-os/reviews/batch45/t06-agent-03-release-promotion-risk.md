# B45-POSTQ4-T06-PROMOTION-DECISION release / promotion risk review

Source status: local release-operator review artifact for Batch 45 T06. This report is not a release action, CI activation, blocker activation, automation activation, provider call, runtime/browser proof, target execution, git action, deployment or publication.

## Scope

Review question:

- Can Batch 45 be promoted to CI/blocker/automation after `B45-POSTQ4-T01..T05B`?
- Which approval boundaries must remain in force?
- What decision, rollback route, next action and forbidden actions should T06 record?

Allowed action boundary for this review:

- Read local source/evidence artifacts.
- Write only this report: `.codex/product-agent-os/reviews/batch45/t06-agent-03-release-promotion-risk.md`.
- Do not change core files.
- Do not run live/model/provider/runtime/browser/target/git actions.
- Do not create CI, blocker enforcement, active automation, release artifacts, tags, PRs, schedules or external writes.

Lifecycle note: `.codex/config.toml` routes Task Brief / Completion Brief through `.codex/workflows/task-plan-lifecycle.md` and control-plane sync through `.codex/workflows/control-plane-sync.md`. The visible Task Brief was shown in chat. `.codex/product-agent-os/lifecycle-state.json` was read but not updated because the current request allowed only this report as a write.

## Sources read

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `.codex/product-agent-os/lifecycle-state.json`
- `PLAN.md`
- `TEST.md`
- `EVALS.md`
- `RUNLOG.md`
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
- `docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json`
- `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
- `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- `.codex/product-agent-os/reviews/batch45/t06-agent-01-source-evidence.md`
- `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md`
- `.codex/artifact-templates/approval-record.md`
- `.codex/artifact-templates/doubt-verification-packet.md`

Memory was used only as orientation to locate current Batch 45 packets. Current release claims below are based on the files read in this review.

## Recommended decision

Recommended T06 decision: `no_go`.

Recommended state string:

`no_go_preserve_advisory_only_static_delta_not_sufficient_for_ci_blocker_automation`

Secondary boundary state:

`approval_required_for_any_future_live_model_runtime_browser_target_ci_blocker_or_automation_promotion`

Rationale:

- T01-T03 produced useful local static cleanup: Q4 warnings went `14 -> 0`, with `blocking=false` and `suppressed_warning_count=0`.
- Static warning cleanup is explicitly not promotion evidence. It does not prove real AI-agent behavior improvement, runtime behavior, browser behavior, rollback safety, target safety, CI safety or automation safety.
- T04 and T05B are approval packets only. T05B was not run and cannot reverse prior no-go decisions.
- T05 used an exact approved live/model route but stopped on baseline timeout after 1 completed primary run and 1 timed-out primary run. Treatment did not run, reviewer did not run and no comparable baseline-vs-treatment table exists.
- M26 remains the strongest live behavior evidence and is no-go: baseline average `4.22`, treatment average `3.88`, treatment worse on 4 of 8 tasks, 1 treatment timeout and independent reviewer `no_go`.
- M27 already rejected CI/blocker promotion and active automation.
- M35 kept advisory-only/no-go for treatment v2 promotion and rejected CI/blocker promotion from fixture-local/static evidence.

## Promotion assessment

| Surface | Decision | Evidence status | Reason |
| --- | --- | --- | --- |
| Local non-blocking advisory | keep | already bounded | M25/M27 allow local non-blocking reversible advisory only. |
| Stronger advisory | no_go | unsupported | No fresh behavior improvement proof after T05; M27 no-go still stands. |
| CI workflow | no_go | unsupported and approval-bound | No CI safety, false-positive, flake, rollback or behavior proof for promoted CI. |
| Blocker enforcement | no_go | unsupported and approval-bound | Static warnings are advisory; promotion threshold requires behavior proof and reviewer non-no-go. |
| Active automation | no_go | unsupported and approval-bound | No schedule/owner/cadence/rollback/monitoring proof; activation was not approved. |
| Runtime/browser pilot | approval_required | missing | Useful only as a future disposable-target approval packet; no runtime/browser action was approved or run. |
| Live/model rerun after T05 | approval_required | T05B packet-only | T05 approval was consumed; T05B requires new exact owner approval before any rerun. |
| Target workspace apply | no_go | unsupported and approval-bound | All current post-Q4 target-like evidence is copied-fixture/static only. |
| Release/deploy/publish | no_go | unsupported and approval-bound | Batch 45 is not release-ready or production-ready from T01-T05B evidence. |

## Approval boundaries that must remain

These surfaces remain forbidden without fresh exact approval naming scope, owner, command/action surface, rollback, evidence and stop conditions:

- provider/model/API calls, including any `codex exec` live/model rerun;
- runtime launch, live server launch and browser automation;
- target workspace commands or mutations;
- database or production/local customer-data access;
- CI workflow creation or mutation;
- blocker enforcement, failing hooks, required checks or policy escalation;
- hook activation in target projects;
- active automation, schedules, recurring jobs or external workflows;
- git branch creation, stage, commit, push, PR, tag or GitHub Release;
- release, deploy, publish, package upload, marketplace/store submission;
- external writes or provider/system mutations;
- retaining raw prompts, raw model traces, provider payload bodies, private source bodies, secrets, credentials or raw private data in repo artifacts.

Approval for one surface must not be reused for another. The consumed T05 live/model approval does not authorize T05B, CI, blocker, automation, runtime/browser, target or git actions.

## Release risks

### P1: CI/blocker promotion would overstate the evidence

T01-T03 reduced static advisory warnings to zero, but T05 did not produce treatment or reviewer evidence. Promoting CI/blocker enforcement would turn a static lint-style signal into a release gate without proof that it improves agent behavior or avoids harmful false positives.

Impact: CI noise, blocked developer workflows, false confidence in behavior quality and audit failure because M26/M27/M35 remain no-go.

### P1: Automation promotion lacks owner/runtime/rollback proof

No active automation was created or validated by T01-T05B. T05 also exposed timeout/flake/cost-control risk. Automation would need owner, cadence, disable path, monitoring, failure handling and evidence retention boundaries before activation.

Impact: runaway provider calls, stale scheduled decisions, external side effects, raw trace retention risk and unclear rollback.

### P1: T05B is easy to misread as approval

T05B is an approval packet only. It is not an executed rerun, not a new owner approval and not promotion evidence.

Impact: accidental provider/model rerun or promotion based on a packet that explicitly says `do_not_run` without new approval.

### P2: Runtime/browser/target behavior remains unproven

Post-Q4 fixes touched copied fixtures and static evidence. No target workspace was run or mutated; no browser/runtime proof exists.

Impact: static cleanup may not preserve real SOL or myPartners behavior.

### P2: Release evidence has retained local-only privacy/path caveats

The security/privacy review found local path retention and hook import-source concerns that should be resolved before any broader promotion or public/team artifact reuse.

Impact: privacy/reproducibility issues and insufficient supply-chain clarity for target hook activation.

## Rollback / disable path

Current T06 recommendation requires no rollout rollback because promotion should not happen.

If an accidental promotion or activation occurs:

1. Disable the local advisory for the affected process/session with `B45_COMMENT_ADVISORY_DISABLED=1`.
2. Remove or disable any newly added CI workflow, required check, blocker hook, schedule or automation created by the accidental promotion.
3. Stop any live/model/runtime/browser/target process started outside approval and record sanitized process-stop evidence.
4. Preserve only sanitized rollup evidence in repo; keep raw model/provider traces out of repo.
5. Revert only files changed by the accidental promotion slice; do not use destructive git operations unless explicitly approved.
6. Record an incident/post-release review packet before reconsidering promotion.

If only this T06 report is rolled back, delete this report file and leave core files unchanged.

## Next action

Recommended next action:

- Record T06 as `no_go` / advisory-only preserved in the owning decision packet or control-plane handoff, without CI/blocker/automation activation.

Optional future routes, each requiring separate approval:

- T05B live/model rerun: new exact approval with model, run count, cost cap, timeout policy, retention, watchdog and stop conditions.
- Runtime/browser disposable pilot: approval packet naming target, commands/browser actions, rollback/delete path, data boundary, provider boundary and evidence artifacts.
- Security/privacy remediation before broader reuse: redact local paths from retained hook evidence and pin/allowlist hook validator import source.
- Source-only treatment v2 design: allowed as planning only; no target apply or promotion.

## Forbidden actions for this T06 closeout

- Do not promote Batch 45 to CI.
- Do not enable blocker enforcement.
- Do not create or enable active automation.
- Do not run T05B.
- Do not reuse the consumed T05 approval.
- Do not claim release-ready, production-ready, runtime-verified, browser-verified, target-safe, behavior-improving or automation-ready.
- Do not stage, commit, push, tag, open PR, deploy, publish or create GitHub Release.
- Do not mutate target projects or call providers/live APIs.

## Control-plane sync decision

- `REQUIREMENTS.md`: `not_applicable`; this review did not change user scope or acceptance.
- `PLAN.md`: `handoff_required`; T06 decision should be recorded by the owner if core control-plane updates are later approved.
- `TEST.md`: `handoff_required`; future promotion checks should include T05B rerun gates, no-absolute-path evidence checks and hook import-source regression if promotion is reconsidered.
- `EVALS.md`: `not_applicable`; no eval threshold changed by this report.
- `RUNLOG.md`: `handoff_required`; detailed evidence belongs in this report, and root file updates were outside the allowed write scope.
- `prod_test.md`: `not_applicable`; Batch 39 surface.
- `RUNLOG.md` overflow decision: `not_checked`; root control-plane mutation was outside this review's write scope.
- Files updated by this task: this report only.

## Handoff

- Release scope: internal Batch 45 promotion decision review for CI/blocker/automation, no external release.
- Artifact list: `.codex/product-agent-os/reviews/batch45/t06-agent-03-release-promotion-risk.md`.
- Evidence status: current local source packets support `no_go`; promotion evidence is missing or contradicted.
- Approval checklist: all live/model/provider/runtime/browser/target/git/release/deploy/publish/CI/blocker/automation surfaces remain approval-bound.
- Rollback/recovery: no rollout should occur; if accidental activation occurs, disable advisory, remove new CI/blocker/automation, stop scoped processes, retain sanitized evidence only and revert only promotion-slice files with approval where needed.
- Control-plane sync decision: `handoff_required` for `PLAN.md`, `TEST.md` and `RUNLOG.md`; other root control-plane files `not_applicable` for this report-only slice.
- Residual risks: no comparable T05 live result, T05B packet-only, M26/M27/M35 no-go still active, no runtime/browser/target proof, local path/hook import-source concerns before broader reuse.
- Exact approval needed for next external action: any T05B rerun, runtime/browser pilot, target command/mutation, CI/blocker activation, automation, git action, deploy/publish or provider call requires a new exact owner approval.
- Recommended next role: owner / lifecycle-orchestrator for recording T06 no-go in the source-owned decision surface, or security/privacy reviewer if path redaction and hook import-source remediation is prioritized before future promotion.
