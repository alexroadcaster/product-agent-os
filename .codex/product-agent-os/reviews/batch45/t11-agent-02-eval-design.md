# B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN eval/test analysis

Source status: independent source-only eval/test design review. No live/model/provider/API, runtime/browser, target command, git, CI/blocker, hook, automation or external action was performed.

Review date: 2026-07-05
Role: independent verification/eval reviewer
Mode: source-only analysis; the only write is this report.

## Scope

- Task: `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN`.
- Output artifact: `.codex/product-agent-os/reviews/batch45/t11-agent-02-eval-design.md`.
- Question: why M26/T05 did not prove behavior improvement, which offline/source-only gates are needed before any new live rerun, and how the next packet should avoid timeout and paired-comparison failure.
- Claim ceiling: `source_design_ready_with_gaps`; this report does not prove treatment v3 works and does not authorize a rerun.

## Sources read

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `.codex/artifact-templates/quality-strategy.md`
- `.codex/artifact-templates/test-eval-matrix.md`
- `.codex/artifact-templates/doubt-verification-packet.md`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
- `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`
- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`
- `.codex/product-agent-os/reviews/batch45/t06-agent-02-test-eval-contract.md`
- `.codex/product-agent-os/reviews/batch45/agent-03-verification-evals.md`

Memory note: `MEMORY.md` was used only as orientation to re-check current Batch 45 source packets. Current repository files above are the evidence source.

## Eval Design Findings

### Finding 1: M26 reduced advisory warnings but did not improve behavior quality

`B45-PCA-M26` remains a no-go. The quantitative result is directionally negative for treatment:

| Metric | Baseline | Treatment | Result |
| --- | ---: | ---: | --- |
| Average local score | `4.22` | `3.88` | treatment lower by `-0.34` |
| Tasks treatment better | n/a | `3/8` | not a majority |
| Tasks equal | n/a | `1/8` | neutral |
| Tasks treatment worse | n/a | `4/8` | regression signal |
| Timeout runs | `0` | `1` | treatment flake/cost regression |
| Advisory warnings | `29` | `15` | static warning improvement only |
| Elapsed seconds | `1724.2` | `2152.11` | treatment slower by `427.91s` |

The promotion threshold failed all three recorded checks:

- treatment average did not exceed baseline by `>=0.5`;
- treatment was not better or equal in the majority of tasks;
- critical failures/blocks were not zero.

The key inference is narrow: M26 proves that the advisory overlay can reduce comment-sufficiency warnings in the evaluated outputs, but it also shows that warning reduction is not a proxy for better task completion, better tests, safer edits or lower flake cost.

### Finding 2: M26 treatment had two evidence integrity failures

Two held-out tasks make the comparison weaker and directionally unfavorable:

- `B45-HELDOUT-02`: treatment ended as `timeout_partial_patch`, `exit_code=124`, `implemented=false`, no advisory collection, and local score collapsed to `1.0`.
- `B45-HELDOUT-07`: treatment completed but `implemented=false`, `changed_file_count=0`, and the packet says the target file was in read-only `.codex`, so this is a no-op rather than a successful behavior change.

Treatment v3 must treat these as design failures, not as random bad luck. Any future eval must pre-classify held-out tasks by writeability, expected command surface, and timeout risk before spending live/model calls.

### Finding 3: T05 cannot supersede M26 because it produced no baseline-vs-treatment comparison

`B45-POSTQ4-T05-LIVE-MODEL-RERUN` stopped on the second baseline task:

| T05 fact | Value |
| --- | --- |
| Planned primary task runs | `16` |
| Approved model task calls started | `2` |
| Completed primary task runs | `1` |
| Timeout primary task runs | `1` |
| Not run due stop rule | `14` |
| Treatment attempted runs | `0` |
| Reviewer calls started | `0` |
| Delta assessment | `not_comparable_due_early_timeout` |

The T05 design used a baseline-first sequence with stop-on-first-timeout. That protected cost, but it destroyed comparability: one timeout prevented the entire treatment arm and reviewer pass. T05 therefore preserves the no-go boundary and adds a fresh flake/cost-control warning.

### Finding 4: The current T05B packet is necessary but not sufficient

`B45-POSTQ4-T05B-RERUN-PACKET-REVISION` correctly records that a new exact owner approval is required and recommends paired order. However, treatment v3 still needs source-only gates before a new approval packet should be considered runnable:

- a source design gate proving the treatment is materially different from the prior noisy generation-time overlay;
- a task feasibility gate proving each held-out task can be edited in the disposable workspace without `.codex` read-only/no-op traps;
- a timeout-risk gate proving known long tasks have a diagnostic route or invalid-pair policy;
- a result-schema gate proving null/timeout/no-op runs cannot be averaged as if they were successful behavior evidence.

## Why Treatment v3 Needs A Different Shape

Treatment v3 should not be "more of the same prompt overlay." The evidence suggests the previous treatment improved comment hygiene in some cases but added planning friction, runtime cost, and failure modes. The safer design is:

- planning scaffold: short checklist before editing, focused on existing capability scan, minimal custom code, test intent and unsupported claim boundaries;
- reviewer scaffold: post-edit self-review rubric that separates behavior quality from comment warning count;
- negative examples: examples of over-commenting, no-op edits, missing tests and unsupported runtime claims;
- hard ceiling: static warning reduction is recorded as secondary evidence only and never promotes by itself;
- source selector: treatment applies only to code tasks where the scaffold maps to the task risk; docs-only/control-plane tasks should not get a code-generation overlay unless the task has code-edit risk.

## Treatment v3 Acceptance Criteria

Treatment v3 is acceptable as source design only when all criteria below are satisfied in a packet before any live rerun approval:

| Criterion | Required evidence | Pass rule |
| --- | --- | --- |
| Treatment identity | Source-owned design packet | Names the exact v3 intervention, trigger, non-goals, old treatment it replaces, fallback and claim ceiling. |
| Behavior mapping | Requirement-to-rubric matrix | Each scaffold item maps to one behavior dimension: existing capability scan, custom code avoidance, test scenario coverage, unsupported claims, privacy/safety or flake/cost control. |
| Prompt friction control | Source-only prompt footprint and placement review | V3 is short, task-local and does not bury the task objective behind broad policy prose. |
| Task suitability | Held-out task feasibility table | All 8 tasks have writeability, expected files, command surface, timeout risk and no-op risk classified before live calls. |
| Timeout policy | Approval-packet-ready decision | Owner must choose `paired_continue_after_timeout` for behavior proof, or accept that `strict_stop_on_first_timeout` means immediate inconclusive/no-go. |
| Pair validity | Result schema contract | Scores are computed only on valid completed pairs; timeout/no-op/null-score pairs are quarantined and reported separately. |
| Promotion threshold | Eval plan | Promotion requires `>=20%` average behavior-quality improvement on valid pairs, treatment equal-or-better on at least `6/8` valid pairs, zero critical regressions, reviewer not `no_go`, and static warning delta not used as behavior proof. |
| Privacy/retention | Retention contract | Raw prompts, raw model traces, provider payloads, private source bodies and secrets remain out of repo; only sanitized rollups and hashes are retained. |
| No premature activation | No-unapproved-actions proof | No CI/blocker/hook/automation/runtime/browser/target/git/provider action is performed while preparing the design. |

## Offline / Source-Only Eval Gates Before Any New Live Rerun

| Gate | Purpose | Minimal source-only check | Blocks live rerun if |
| --- | --- | --- | --- |
| `G1-source-freeze` | Prevent moving-target evals | Record hashes for task plan, v3 design, approval packet, workflow/checklist and scoring rubric. | Any source is missing, mutable or mismatched. |
| `G2-v3-diff-from-old-treatment` | Ensure v3 is a real design change | Compare old treatment failure classes to v3 mitigations. | V3 only adds more advisory prose or relies on warning reduction. |
| `G3-heldout-feasibility` | Avoid no-op/read-only failures | Table for all 8 tasks: allowed files, expected edit surface, `.codex` writeability, needed commands, timeout risk. | Any task has unresolved writeability/no-op risk and no replacement/invalid-pair rule. |
| `G4-timeout-forensics` | Avoid repeating T05 | Source-only analysis of M26/T05 timeout tasks, stderr-size signal, known wrapper failures and process-stop evidence. | Root cause is unknown and the packet still uses baseline-first or global stop-on-timeout for promotion proof. |
| `G5-paired-run-simulator` | Validate comparability before live calls | Dry source-only schedule: per task pair, arm order, timeout handling, reviewer timing and stop rules. | A single timeout can erase the whole treatment arm again. |
| `G6-result-schema-negative-tests` | Prevent bad averaging | Assert timeout/no-op/null-score treatment rows cannot contribute to behavior averages. | Invalid pairs can be averaged as score `1.0` or silently omitted without denominator disclosure. |
| `G7-rubric-calibration` | Separate behavior from comments | Define behavior score, static warning score, reviewer decision and critical regression flags separately. | Static advisory warning delta can promote or override behavior no-go. |
| `G8-cost-retention-approval` | Keep live approval exact | Packet names model, call cap, cost cap or accepted cost gap, temp root, raw retention, process kill, lingering process check. | Any provider/model/cost/retention/process boundary is ambiguous. |
| `G9-no-unapproved-actions` | Preserve approval boundary | Source packet explicitly lists forbidden surfaces and current no-action evidence. | The design requires live/model/runtime/browser/target/git/CI/automation work without exact approval. |

## Timeout And Paired-Comparison Design

Recommended policy for a future behavior-proof rerun is `paired_continue_after_timeout`, not baseline-first strict stop:

1. For each held-out task, run one baseline and one treatment in the same task pair before moving to the next task.
2. If either arm times out, mark the pair `invalid_timeout_pair`; do not include it in average behavior score.
3. Continue until the approved call cap is reached or until valid-pair count can no longer satisfy the promotion threshold.
4. Stop with no-go if valid completed pairs fall below the minimum sample threshold.
5. Run the independent reviewer only after enough valid pairs exist; reviewer receives sanitized per-pair summaries, invalid-pair ledger and unsupported-claims list.

Minimum sample rule:

- promotion-quality proof should require `8/8` valid pairs;
- `7/8` may support "needs reviewer / rerun one pair" only if the invalid pair is not treatment-specific and no critical regression exists;
- `<=6/8` is diagnostic-only and cannot promote.

This avoids the T05 failure mode: one early baseline timeout no longer erases the treatment arm, and invalid data cannot masquerade as a completed comparison.

## Future Live Approval Prerequisites

Before any future live/model/provider rerun, a new approval packet must include:

- exact provider surface and model;
- exact maximum primary calls and reviewer calls;
- selected timeout policy, with `paired_continue_after_timeout` recommended for behavior proof;
- external watchdog, process-tree kill, timeout marker and lingering-process check;
- disposable temp root and write-probe/cleanup safety;
- raw-output temp-only retention and repo-safe sanitized rollup fields;
- no target workspace mutation, runtime/browser launch, database access, git action, CI/blocker promotion or automation;
- result schema with per-pair validity, no-op detection, timeout quarantine, static warning counts and behavior scores separated;
- acceptance threshold and reviewer route;
- abort conditions for ambiguous cost, unsafe cleanup, unresolved writeability, raw trace persistence or unapproved surfaces.

Without that packet and exact owner approval, the only valid state is `approval_required_not_run`.

## Verification Commands / Gaps

Commands run in this source-only review:

| Command | Exit code | Evidence |
| --- | ---: | --- |
| `Get-Content -LiteralPath .codex\config.toml` | `0` | Lifecycle contract and approval boundaries loaded. |
| `Get-Content -LiteralPath .codex\workflows\task-plan-lifecycle.md` | `0` | Task Brief / Completion Brief workflow loaded. |
| `Get-Content -LiteralPath .codex\workflows\control-plane-sync.md` | `0` | Control-plane sync workflow loaded. |
| `rg -n "Batch 45|B45|POSTQ4|T11|M26|T05|treatment v3" C:\Users\user\.codex\memories\MEMORY.md` | `0` | Orientation only; current source files rechecked. |
| `Get-Item` for the four requested JSON packets | `0` | All requested packet files were present. |
| `Get-Content` for the four requested JSON packets | `0` | Source evidence read. |
| `Get-Content` for `quality-strategy.md`, `test-eval-matrix.md`, `doubt-verification-packet.md` | `0` | Verification template constraints read. |
| `python -c "...json.loads..."` over the four requested JSON packets | `0` | Current parse/status summary succeeded. |
| `python -c "...M26 quantitative..."` | `0` | M26 quantitative no-go fields extracted. |
| `python -c "...T05 execution..."` | `0` | T05 timeout/comparison failure fields extracted. |

Accepted gaps for this review:

- No live/model/provider/API rerun: forbidden by current task.
- No runtime/browser/target commands: forbidden by current task.
- No git/CI/blocker/automation checks: forbidden by current task.
- No lifecycle marker write: user constrained writes to this single review file.
- No root control-plane updates: this task is source-owned review output only; root sync is handoff-required if the owner wants T11 promoted into `PLAN.md`, `TEST.md` or `EVALS.md`.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; this review does not change accepted project scope.
- `PLAN.md`: `handoff_required`; if T11 becomes the next executable queue item, add a compact pointer only.
- `TEST.md`: `handoff_required`; offline/source-only gates above should be promoted only if the owner wants them as canonical verification commands.
- `EVALS.md`: `handoff_required`; treatment v3 thresholds and invalid-pair policy belong there if adopted.
- `RUNLOG.md`: `not_applicable_for_this_write_scope`; detailed evidence is in this source-owned review to avoid root bloat.
- `prod_test.md`: `not_applicable`; Batch 39 ledger is out of scope.

## Handoff

- Verdict: `revise_before_live_rerun`.
- Current evidence: M26 no-go remains decisive; T05 is inconclusive/no-go and cannot supersede M26.
- Unsupported claims: treatment v3 improves behavior; static warning reduction proves better code; future live rerun is approved; CI/blocker/runtime/browser/target readiness exists.
- Required next artifact: a source-owned treatment v3 design packet plus updated approval packet with paired-continue timeout policy.
- Recommended next role: test/eval designer or implementation planner for T11 source packet; release/promotion decision remains no-go until a future approval-bound live rerun produces valid paired evidence.
