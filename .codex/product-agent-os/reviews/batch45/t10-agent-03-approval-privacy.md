# B45 Post-Q4 T10 Approval / Privacy Review

Source status: local independent review artifact.

## Scope

Task: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET` privacy and approval-boundary review.

Allowed action boundary for this review:

- read current local source-truth packets and lifecycle/config artifacts;
- write exactly this report file;
- no live/model/provider/runtime/browser/target/git/CI/automation action;
- no target workspace command, mutation, database access, release, deploy, publish, hook activation or external write.

Lifecycle note: `.codex/config.toml` routes Task Brief / Completion Brief through `.codex/workflows/task-plan-lifecycle.md` and control-plane sync through `.codex/workflows/control-plane-sync.md`. The visible Task Brief was shown in chat. `.codex/product-agent-os/lifecycle-state.json` was not edited because the user allowed exactly one report file.

## Sources Read

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json`
- `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`
- `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`
- `docs/superpowers/specs/batch45-post-q4-next-tasks.json`
- `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json`
- `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json`
- prior scoped review: `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md`

Memory was used only to orient to current Batch 45 packets; all review conclusions below are based on current files read in this run.

## Findings

### P0

No P0 findings.

### P1

No P1 findings.

### P2

#### P2-01: Future T10 rerun must not treat call-count-only cost control as a complete cost cap

Evidence:

- M26 recorded real provider usage but no actual USD cost: `provider_cost_usd: null` and `actual_usd_cost_not_available_from_cli_output` in `docs/superpowers/specs/batch45-agent-behavior-eval-results.json:50` and `:56-57`.
- T05 ran with `cost_cap: accepted_gap_cost_unavailable_call_count_cap_only` in `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json:21`.
- T05B correctly requires `cost_cap: <USD cap> or accepted_gap_cost_unavailable_call_count_cap_only` in `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:33`.

Assessment:

This is not an approval-boundary violation in the current packet because the accepted-gap path is explicit. It is still a material residual risk for T10: if the owner does not provide a concrete USD cap, the approval packet must label the run as call-count-capped only and must not call it full budget enforcement.

Required T10 handling:

- Require either a concrete USD cap or an explicit owner statement accepting `accepted_gap_cost_unavailable_call_count_cap_only`.
- Preserve run-count caps separately from USD budget.
- Abort if the owner response is ambiguous about model, run count, timeout policy or cost cap.

### P3

#### P3-01: Raw timeout forensics remain temp-only and cannot become source evidence

Evidence:

- T05 stores only sanitized rollup in repo and records `raw_outputs_location: temp_only` for both completed and timed-out runs in `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json:105` and `:154`.
- T05 timeout stderr was large (`stderr_length_bytes: 6270806`) but represented only by hashes/metadata in repo at `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json:159`.
- T05B forbids repo retention of raw prompts, raw model traces, provider payload bodies, private source bodies, secrets and credentials in `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:73-85`.

Assessment:

The current retention boundary is sound. The T10 packet should explicitly keep timeout-root-cause inspection as optional temp-only forensics, with sanitized summary only. Raw stderr/stdout/prompts must not be copied into repo, reports, fixtures, evals, screenshots, generated site or memory.

## Approval Packet Field Review

T05B already contains the right exact-approval field set for a redesigned T10 packet:

- provider/model/surface and command surface: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:20-31`;
- run count, reviewer count and setup/smoke count: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:23-29`;
- disposable temp root, timeout and overall wall-clock policy: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:31-33`;
- cost cap and retention fields: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:33-35`;
- reviewer route and timing: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:36`.

T10 should preserve those fields and add an explicit owner-choice field for the timeout mode:

- `strict_stop_on_first_timeout`;
- `paired_continue_after_timeout`;
- `single_task_diagnostic`;
- any retry-on-timeout mode, if introduced, with exact retry count and cost impact.

Default without new exact approval remains `do_not_run`, per `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:17-18`.

## Privacy And Data Exposure Status

- No current source packet authorizes raw private prompt/model/provider payload retention in repo.
- T05B repo-allowed retention is limited to sanitized scores, timeout markers, hashes, changed-file metadata and aggregate token/cost/call counts if available: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:73-82`.
- T05B repo-forbidden data includes raw prompts, raw model traces, provider payload bodies, private source bodies, secrets and credentials: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:83-85`.
- T11 is source-only and performed no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation action: `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json:7-8`.

Data exposure status: no high-confidence secret, credential, raw private data, raw provider payload or raw model trace retention found in the scoped T10 source truth.

## Process And Timeout Boundary

T05B has the right watchdog contract:

- `outer_non_model_watchdog_required: true`;
- `process_tree_kill_on_timeout: true`;
- `timeout_marker_required: true`;
- `lingering_process_check_required: true`;
- forbidden silent timeout retries, raw repo retention, target workspace mutation and provider/model calls outside exact approved count.

Evidence: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:60-70`.

T05 result also records scoped process stop evidence and no remaining external temp fixture after stop in `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json:144-151`; the approved stop after timeout is recorded at `:217`.

T10 should make process-tree kill and lingering-process verification mandatory result fields, not optional notes.

## Forbidden Surfaces

Forbidden or approval-required surfaces remain correctly blocked in current source truth:

- T05B no live/model/provider call occurred: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:5-7`.
- T05B no-unapproved-actions booleans are all false for live/model/provider, runtime/browser, target, database, CI/blocker, git, release/deploy/publish, automation and external writes: `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json:115-127`.
- Post-Q4 queue states T10 must stop before live/model/provider/API call without exact owner approval: `docs/superpowers/specs/batch45-post-q4-next-tasks.json:296` and `:316`.
- T10 acceptance explicitly requires no model/provider/API call while preparing the packet: `docs/superpowers/specs/batch45-post-q4-next-tasks.json:307-308` and `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json:122-123`.

Approval boundary status: acceptable for packet-only work. Any execution after T10 requires a new exact approval packet and cannot reuse T05 approval.

## Claim Ceiling

Current ceiling remains:

- M26 no-go is active: baseline `4.22`, treatment `3.88`, treatment worse on 4 of 8 tasks, one timeout and reviewer `no_go`.
- T05 stopped on baseline timeout with no treatment/reviewer comparison.
- T05B is approval-packet-only.
- T11 is source-only treatment design, not behavior proof.

T10 cannot claim behavior improvement, runtime/browser readiness, target safety, CI/blocker readiness, active automation, release/deploy/publish readiness, or reversal of M26/M35/T05/T06.

## Missing Tests / Future Gate Recommendations

Before any future approved T05B-style run, add or require these checks in the T10 packet:

- approval-packet assertion that either concrete `max_cost_usd` or explicit call-count-only accepted gap is present;
- result-schema assertion that timeout/no-op/null-score pairs are quarantined from promotion metrics;
- retention assertion that raw prompts, traces, provider payloads, raw stderr/stdout and private source bodies are not written under repo paths;
- process-tree assertion that timeout marker, kill result and lingering-process check are present per run;
- no-unapproved-actions assertion covering live/model/provider outside count, runtime/browser, target command/mutation, database, CI/blocker, git, release/deploy/publish, automation and external write;
- source-freeze assertion for eval plan, task prompts, scoring rubric, treatment contract and approval packet.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; scope and acceptance did not change.
- `PLAN.md`: `handoff_required`; T10 implementation owner should add a compact pointer only if the actual T10 packet is created.
- `TEST.md`: `handoff_required`; future T10 packet should own the approval/privacy/no-unapproved-actions assertions listed above.
- `EVALS.md`: `not_applicable`; no eval threshold was changed by this review.
- `RUNLOG.md`: `handoff_required`; no direct update allowed and detailed evidence belongs in this report.
- `prod_test.md`: `not_applicable`.
- `RUNLOG.md` overflow decision: `not_checked`; root control-plane mutation was outside the allowed write scope.

## Commands Run

Read-only commands only:

- `Get-Content` for security skill, `.codex/config.toml`, lifecycle/control-plane workflows and Batch 45 source packets.
- `Select-String` over memory registry for orientation.
- `rg --files` and scoped `rg -n -F` over Batch 45 source packets.
- `Get-ChildItem` for scoped existing Batch 45 review artifact discovery.
- `Test-Path` for the target report path.

No live/model/provider/runtime/browser/target/git/CI/automation command was run.

## Completion Brief

- Task ID: `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET`
- Result status: `review_complete_packet_only_with_residual_cost_gap`
- What was done: reviewed T05, T05B, T11, post-Q4 next-task, T08 and M26 source truth for approval/privacy boundaries.
- Files / artifacts changed: `.codex/product-agent-os/reviews/batch45/t10-agent-03-approval-privacy.md` only.
- Verification evidence: local read-only inspection of named packets; report created as the only write; no forbidden surfaces used.
- Residual risks / accepted gaps: no live execution proof; no broad secret scan; lifecycle marker/control-plane files not edited due exact one-file write scope; cost cap can remain call-count-only only with explicit owner acceptance.
- Follow-up: Plugin Runtime Builder or Eval/Test Engineer should encode the cost/retention/process-kill/no-unapproved-actions assertions when creating the actual T10 packet; Completion Skeptic should review before any new exact approval is requested.
