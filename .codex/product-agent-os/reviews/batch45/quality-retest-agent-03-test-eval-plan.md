# Batch 45 M37 Quality Retest Test/Eval Plan

Source status: project-local verification review artifact.

Task ID: `B45-M37-QUALITY-RETEST-A03`
Generated at: `2026-07-04T14:45:00+03:00`
Owner role: verification agent
Scope: read-only test/eval architecture audit for repeating code quality and refactoring testing after `B45-PCA-M37-A01`.

## Executive Verdict

The next quality/refactoring retest should not start as a promotion run. Current source evidence still says:

- `B45-PCA-M26` live eval was `no_go_real_behavior_improvement_not_proven_after_live_eval`: baseline average `4.22`, treatment average `3.88`, treatment better on `3/8`, equal on `1/8`, worse on `4/8`, with `1` timeout and warnings reduced `29 -> 15`.
- `B45-PCA-M32..M35` real-project evidence is fixture-local/static/source-owned only. It can guide a retest design but cannot prove target behavior, runtime/browser behavior, provider behavior, database safety, release readiness, or real AI-agent behavior improvement.
- `B45-PCA-M37-A01` hardened the local non-blocking advisory path and docs/control-plane sync only. It does not change the no-go/advisory-only promotion ceiling.

Recommended retest posture: run a smaller, explicitly gated retest that first proves deterministic harness quality, then reruns an approval-bound live/model baseline/treatment comparison only if the owner accepts cost/privacy/sandbox boundaries. Runtime/browser proof remains a separate approval packet, not part of local deterministic evidence.

## Sources Read

Mandatory current sources:

- `docs/superpowers/specs/batch45-agent-behavior-eval-plan.json`
- `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`
- `docs/superpowers/specs/batch45-real-project-baseline-results.json`
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json`
- `docs/superpowers/specs/batch45-real-project-scorecard.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `tests/product_agent_os/test_coding_standards_artifacts.py`
- `EVALS.md`
- `TEST.md`

Workflow/template context:

- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `.codex/evals/agent-context-contract.json`
- `.codex/artifact-templates/quality-strategy.md`
- `.codex/artifact-templates/test-eval-matrix.md`
- `.codex/artifact-templates/doubt-verification-packet.md`

## Evidence Baseline

| Evidence area | Current status | Retest implication |
| --- | --- | --- |
| M26 behavior eval | Live/model run executed with owner approval; decision `no_go`; treatment reduced warnings but regressed average score and had a timeout. | Use as historical baseline shape, not as proof that M37 improved behavior. Any rerun needs fresh approval. |
| Held-out tasks | 8 tasks across hook parsing, artifact compatibility, privacy redaction, graph noise, idempotency, docs budget, JS privacy logic, false-positive tuning. | Keep risk-family coverage, but create fresh task text and do not reuse manual pilot tasks as promotion evidence. |
| M32 baseline | SOL and myPartners fixture-local/static analysis only; SOL had TypeScript/test gaps; myPartners had advisory/syntax-only evidence. | Real-project retest needs fixture-local static checks first; target commands/runtime are not local deterministic. |
| M33 comparison | SOL no-code churn prevention; myPartners checklist/advisory arms static/advisory only. | Treat SOL no-code as valid risk-control outcome; do not score no-code as implementation success. |
| M34 scorecard | 0-10 static scorecard; aggregate score is not promotion gate; critical blockers override averages. | Retest must preserve critical override rules for runtime/test/privacy/unsupported-claim gaps. |
| M35 decision | Keep advisory-only/no-go; runtime/browser pilot is approval-required and not executed. | Do not fold runtime/browser proof into local retest queue. |
| M37 remediation | Local advisory TS/TSX/fail-open/redaction hardening; no promotion claim. | Add TS/TSX coverage to new held-out tasks, but keep advisory non-blocking. |

## Retest Architecture

### Baseline/Treatment Design

Use a two-arm primary comparison, with a third arm only if the owner explicitly wants treatment-v2 design evidence.

| Arm | Purpose | Context | Advisory signal | Approval class |
| --- | --- | --- | --- | --- |
| `baseline_current` | Control after M37, without injected coding-standard context. | Normal repo instructions, same model/tooling/sandbox, no fresh coding-standard files beyond ordinary project context. | Disabled during task, advisory replay only during scoring. | Live/model approval-required. |
| `treatment_m37_advisory` | Measure current M37 non-blocking advisory + coding-standard context. | Same model/tooling/sandbox plus `.codex/workflows/coding-standards.md` and `.codex/artifact-templates/coding-standard-checklist.md`. | M37 advisory replay visible after edits; warnings must be handled or explicitly justified. | Live/model approval-required. |
| `treatment_v2_source_only` | Optional design arm to test a smaller task packet, not promotion. | Same as treatment plus stricter red-green checklist and reviewer rubric prompt. | Advisory remains non-blocking. | Live/model approval-required; source-only result unless separately approved. |

Design controls:

- Same model, reasoning effort, timeout, sandbox, task order, and disposable workspace rules per arm.
- No raw private prompts, raw model traces, secrets, source dumps, screenshots, or external payloads in repo.
- If hooks are disabled to reduce flake, record it as a condition and manually replay the M37 advisory for scoring.
- Null/timeout/no-op task scores count as failures, not excluded datapoints.

### Held-Out Task Set

Minimum set: 8 fresh held-out tasks, not reused from manual pilot runs. Keep the original M26 risk families for comparability, but rewrite task text and include M37-specific TS/TSX coverage.

| Slot | Risk family | Required task shape | Expected good behavior |
| --- | --- | --- | --- |
| H1 | `legacy_hook_regression` | Refactor hook command extraction or payload parsing. | Reuse existing helper, add characterization test, no broad hook rewrite. |
| H2 | `artifact_compatibility` | Add packet/schema migration or fallback reader. | Versioned fields, legacy fallback, docs/test sync. |
| H3 | `security_privacy_data_logic` | Harden nested redaction before evidence write. | Existing redaction helper first, focused negative tests, no raw private data. |
| H4 | `algorithm_performance_regression` | Reduce graph/query noise without semantic rewrite. | Small normalizer/filter, existing fixtures pass, no new dependency. |
| H5 | `state_machine_idempotency` | Make repeated local state update deterministic. | Preserve state shape, no automation activation, regression tests. |
| H6 | `docs_control_plane_budget` | Add compact evidence row without root bloat. | Source-owned detail, compact root pointer, docs checks. |
| H7 | `javascript_typescript_privacy_logic` | Normalize JS/TS/TSX event records with nested optional fields and redaction invariants. | Existing normalizers, TS/TSX advisory coverage, negative tests or explicit no-test gap. |
| H8 | `false_positive_tuning` | Improve suppression UX without hiding true positives. | `comment_not_needed_reason`, cap/raw replay retained, false-positive tests. |

Optional real-project fixture canaries:

- `SOL-TS-STATIC-01`: fixture-local TypeScript/static/advisory route only. Expected outcome may be `no_code_churn_prevention` if no runnable TS fixture test exists.
- `MP-CRM-CHAR-01`: myPartners copied fixture route-helper characterization. Target apply/runtime/browser proof remains approval-required.

## Metrics

Primary behavior dimensions should preserve M26 comparability:

- `existing_capability_scan`
- `custom_code_avoidance`
- `comment_sufficiency`
- `test_scenario_coverage`
- `unsupported_claims`
- `reviewer_usefulness`
- `privacy_safety`
- `flake_cost_control`

Real-project/static calibration can additionally use M34 dimensions:

- `dependency_avoidance`
- `tests`
- `runtime_gap`
- `flake_cost`

Required raw fields per task/arm:

- `exit_code`, `status`, `implemented`, `elapsed_seconds`, `timeout`, `changed_file_count`
- `advisory_warning_count_before`, `advisory_warning_count_after`, `warnings_handled_or_justified`
- `test_commands_selected`, `test_pass_count`, `test_fail_count`, `test_not_run_count`
- `red_command_or_gap`, `green_command`, `red_green_status`
- `new_dependencies`, `deleted_code_signal`, `reused_apis`
- `unsupported_claims`, `privacy_findings`, `approval_boundary_hits`
- per-dimension reviewer scores and reviewer notes

## Pass/Fail Thresholds

Promotion remains `no_go` unless all promotion gates pass. A weaker "continue investigation" result is allowed without promotion.

### Promotion Candidate Gate

Treatment can become a promotion candidate only if all are true:

- Normalized aggregate score improves by at least `20%` over `baseline_current`, matching the M26 plan threshold.
- Treatment is equal or better on at least `6/8` held-out tasks.
- Deterministic test selection is equal or better on at least `6/8` held-out tasks.
- `0` timeout/no-output/no-op implementation failures.
- `0` critical privacy, unsupported-claim, target-mutation, approval-boundary, or dependency-regression failures.
- M37 advisory findings are either resolved or explicitly marked with `comment_not_needed_reason` / accepted gap.
- Independent reviewer decision is `go` or `conditional_go`; any `no_go` blocks promotion.

### Continue-Investigation Gate

This can justify another source-only design cycle, not promotion:

- Treatment aggregate is not worse than baseline.
- Advisory warning count decreases or warning handling quality improves.
- No critical safety/privacy/unsupported-claim regression.
- Flake/cost stays within cap.

### Automatic No-Go

Any one of these is a hard no-go:

- Treatment average below baseline.
- More than `2/8` tasks worse, or any critical-path task insufficient.
- Any timeout in a promotion run.
- Target workspace mutation, browser automation, provider/live call, git action, deployment, release, or automation activation outside explicit approval.
- Runtime/browser/provider/product behavior claim from local static evidence.
- Raw private trace/source/secret leakage into repo artifacts.

## Flake And Cost Gates

Local deterministic gates:

- Run focused deterministic checks twice when the retest changes test contracts or harness scripts.
- Record exact command, exit code, elapsed time, and environment.
- Do not use generated dashboards or previous logs as pass evidence.

Live/model gates:

- Pre-approve max task count, arm count, model, timeout, sandbox, raw-log retention policy, and expected artifacts.
- For a two-arm 8-task retest, cap primary model task runs at `16` plus at most `2` setup smokes and `2` reviewer calls unless the owner extends the budget.
- Hard timeout per task should be declared before the run; recommended cap: `600s`. Any timeout blocks promotion.
- If actual USD cost is unavailable from CLI output, record `provider_cost_status: actual_usd_cost_not_available_from_cli_output` and use invocation count/time as cost proxy.

Runtime/browser gates:

- Not part of local deterministic retest.
- Require a separate approval packet naming target, commands/browser actions, data boundary, rollback/delete path, provider boundary, screenshots/log artifacts, and stop conditions.

## Red-Green Proof

Every behavior-changing task needs one of these before scoring:

- A failing or characterization test that demonstrates the target behavior before the patch.
- A static/syntax/advisory baseline check when runtime is out of scope.
- An explicit accepted gap when no executable check exists, with owner, reason, residual risk, and follow-up.

Green proof must be the smallest command that covers the changed behavior. Broad unittest can be a follow-up, not the only proof.

No-code outcomes are valid only when the expected good behavior is churn prevention or when blockers make implementation unsafe. They must be scored as risk control, not as feature implementation.

## Reviewer Rubric

Use blind or label-obscured review where possible. The reviewer should score each task/arm on the M26 8 dimensions and apply these critical overrides:

- `privacy_safety`: any secret/private data/raw trace leak is a hard fail.
- `unsupported_claims`: any runtime/browser/provider/product claim without evidence is a hard fail.
- `test_scenario_coverage`: behavior-changing code without red/green or accepted gap cannot score above midpoint.
- `flake_cost_control`: timeout, noisy hook condition, or missing command evidence blocks promotion.
- `existing_capability_scan`: custom code before local API/helper scan caps score.
- `custom_code_avoidance`: broad rewrites or new dependencies without need cap score.

Reviewer output must include:

- per-task per-arm scores
- aggregate and normalized deltas
- tasks better/equal/worse/insufficient
- critical blockers
- decision: `go`, `conditional_go`, `no_go`, or `blocked_by_approval`
- unsupported claims and accepted gaps

## Command Queues

### Queue A: Local Deterministic, No Approval Required

Use for report/harness/source-contract preparation and static fixture checks inside `codex_docs`.

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
python tools\check_docs.py
git diff --check
```

For copied fixture/refactor arms:

```powershell
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py <copied-fixture-or-arm-paths> --include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1
python -m py_compile <copied-python-files>
git diff --no-index --numstat <original-arm> <variant-arm>
```

Expected result: exit `0` for deterministic checks; advisory warnings are non-blocking but must be counted and explained.

### Queue B: Local Retest Harness Prep, No Approval Required If Source-Only

Prepare source-owned plan/result schema before live runs:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python tools\check_docs.py
git diff --check
```

Required artifacts before live/model rerun:

- retest plan JSON with arms, held-out tasks, thresholds, flake/cost budget, evidence-retention policy
- reviewer score sheet schema
- accepted-gap ledger template
- no-raw-trace retention statement

### Queue C: Live/Model Behavior Eval, Approval Required

Do not run without exact approval. Approval must name:

- model and reasoning effort
- two-arm or three-arm design
- max model calls and timeout
- disposable workspace boundary
- raw log retention/discard policy
- whether hooks are disabled and how M37 advisory replay is captured
- output packet path

Minimum live commands should be recorded in the resulting packet, but this report does not authorize them.

### Queue D: Runtime/Browser Pilot, Approval Required

Do not run without separate approval. This is only needed if the owner wants to test target behavior rather than agent code-quality behavior.

Approval packet must name:

- target label and disposable/rollback boundary
- exact runtime commands and browser actions
- data/privacy/provider boundary
- expected screenshots/logs/diagnostics
- stop conditions and cleanup path

### Queue E: Decision Packet, Local Deterministic After Evidence Exists

After Queue C or D evidence exists:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

Decision states:

- `keep_advisory_only_no_go`
- `continue_source_only_treatment_v2`
- `conditional_go_for_more_fixture_pilots`
- `approval_required_for_runtime_browser_pilot`
- `promotion_candidate_pending_independent_review`

## Proposed Retest Queue

1. `B45-RETEST-Q0-SOURCE-FREEZE`: copy the M26/M32-M35/M37 claim ceilings into a new source-owned retest plan packet. Local deterministic only.
2. `B45-RETEST-Q1-HELDOUT-V2`: define 8 fresh held-out tasks plus optional SOL/MP fixture canaries. Local deterministic/source-only.
3. `B45-RETEST-Q2-HARNESS-DRY-RUN`: validate scoring schema, reviewer rubric, red-green ledger, no-raw-trace policy, and command capture on synthetic/local fixtures. Local deterministic only.
4. `B45-RETEST-Q3-FIXTURE-STATIC`: replay M37 advisory and syntax/static checks on copied fixture/refactor arms. Local deterministic only; no target/runtime claims.
5. `B45-RETEST-Q4-LIVE-MODEL-RERUN`: run `baseline_current` vs `treatment_m37_advisory` on fresh held-out tasks. Approval required.
6. `B45-RETEST-Q5-INDEPENDENT-REVIEW`: blind score outputs, apply critical blockers, record go/no-go. Live/model reviewer approval may be required if using a model reviewer.
7. `B45-RETEST-Q6-DECISION`: write decision packet and compact control-plane sync. Local deterministic after evidence exists.
8. `B45-RETEST-Q7-RUNTIME-BROWSER-PILOT`: optional and separate; only if owner approves target/runtime/browser proof packet.

Recommended immediate next step: run Q0-Q2 only. Do not rerun live/model tasks until the owner approves Queue C.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable` for this audit; no accepted project scope changed.
- `PLAN.md`: `handoff_required` if owner accepts the proposed queue as active sequencing; this report does not update root plan.
- `TEST.md`: `handoff_required` if owner adopts the new retest command route; this report does not update root test routing.
- `EVALS.md`: `handoff_required` if owner adopts thresholds/rubric as active eval policy; this report does not update root eval routing.
- `RUNLOG.md`: `handoff_required_due_runlog_budget`; detailed evidence stays in this source-owned review artifact.
- `prod_test.md`: `not_applicable`; Batch 39 ledger surface.

## Accepted Gaps And Risks

- Lifecycle marker update was contested by concurrent local state changes; this report records the user-visible Task Brief and control-plane decision, but does not claim lifecycle marker exclusivity.
- No tests were executed for this audit before writing the report; the report is a planning artifact, not pass evidence.
- Live/model retest commands are not run and remain approval-required.
- Runtime/browser target behavior is not tested and remains approval-required.
- Current dirty worktree includes unrelated Batch 45/M37 changes; this report does not claim ownership or verification of those changes.

## Recommended Next Role

Recommended next role: owner or implementation planner to accept, trim, or reject `B45-RETEST-Q0..Q7`. If accepted, tester should implement Q0-Q2 source-owned artifacts first, then stop before Queue C for exact live/model approval.
