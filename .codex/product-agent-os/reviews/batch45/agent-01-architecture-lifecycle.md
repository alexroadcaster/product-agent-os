# Batch 45 Architecture Lifecycle Review

Source status: independent read-only architecture audit.

## Scope

Reviewed Batch 45 Professional Code Authoring / S7 scenario harness architecture in `C:\Users\user\Desktop\project\codex_docs`.

Focus:

- architecture boundaries for Professional Code Authoring, advisory hooks, S7 real-project scenario harness, fixture-local evidence, scorecard and decision packets;
- lifecycle and `closure_level` integrity;
- activation/fallback proof boundaries;
- source-owned evidence flow across S0-S7;
- M24-M35 gate sequencing;
- fit with Product-Agent OS control-plane architecture;
- architecture debt and verification gaps.

This review did not change code, docs, registry, git, hooks or runtime. The only write performed by this reviewer is this report.

## Sources read

Lifecycle and control-plane routing:

- `.codex/config.toml` (`[product_agent_os.lifecycle_contract]`, `[workflows]`)
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `.codex/workflows/coding-standards.md`
- `.codex/artifact-templates/coding-standard-checklist.md`
- `.codex/product-agent-os/lifecycle-state.json`

Control-plane and project source truth:

- `AGENTS.md`
- `REQUIREMENTS.md`
- `PLAN.md`
- `TEST.md`
- `EVALS.md`
- `RUNLOG.md`
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`

Batch 45 architecture and S7 source-owned evidence:

- `research/batch45-professional-code-authoring-architecture-v2.md`
- `research/batch45-professional-code-authoring-solution-map.md`
- `research/b45-real-project-scenarios/README.md`
- `research/b45-real-project-scenarios/source-policy.md`
- `research/b45-real-project-scenarios/source-inventory.md`
- `research/b45-real-project-scenarios/scenario-candidates.json`
- `research/b45-real-project-scenarios/schemas/fixture-manifest.schema.json`
- `research/b45-real-project-scenarios/schemas/redaction-manifest.schema.json`
- `research/b45-real-project-scenarios/fixtures/sol-agent-orchestration/*`
- `research/b45-real-project-scenarios/fixtures/mypartners-crm-chat-open/*`
- `research/b45-real-project-scenarios/results/*`
- `docs/superpowers/specs/batch45-real-project-baseline-results.json`
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json`
- `docs/superpowers/specs/batch45-real-project-scorecard.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- related `docs/superpowers/specs/batch45-*.json` packets for S0-S6/M24-M27

Implementation and enforcement surfaces inspected read-only:

- `.codex/hooks.json`
- `.codex/hooks/hooks.json`
- `.codex/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/product_agent_os/tools/comment_sufficiency.py`
- `plugins/product-agent-os/product_agent_os/self_learning_candidates.py`
- `plugins/product-agent-os/product_agent_os/automation_policy.py`
- `plugins/product-agent-os/product_agent_os/codex_runtime_runner/routes.py`
- `plugins/product-agent-os/product_agent_os/discovery.py`
- `plugins/product-agent-os/product_agent_os/status_dashboard.py`
- `plugins/product-agent-os/assets/templates/workflows/coding-standards.md`
- `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md`
- `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md`
- `plugins/product-agent-os/assets/templates/operations/hook-governance.md`
- focused tests under `tests/product_agent_os/` covering automation policy, self-learning candidates, discovery/docs routing and behavioral workflow artifacts

## Current architecture state

Batch 45 currently has a conservative, source-owned architecture:

- S0-S6 establish Professional Code Authoring as an advisory, evidence-producing capability, not an enforcement or promotion mechanism. `PLAN.md:34` records S0-S6 as docs/contract/synthetic/local advisory evidence and keeps M27 as no-go for CI/blocker promotion.
- M24-M27 are sequenced as false-positive audit, tuning, approved local non-blocking PostToolUse advisory, held-out eval, and promotion/no-go. `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md:468-476` records M24 warning reduction, M25 local advisory replay, M26 held-out eval result, and M27 no-go.
- S7/M28-M35 add a real-project scenario harness that remains source-only and fixture-local. `PLAN.md:35` and `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md:411-419` define M28-M35 from architecture atlas through decision packet, with runtime/browser pilot deferred to M36.
- The S7 harness keeps target projects read-only and copies only sanitized analysis-only fixtures. `research/b45-real-project-scenarios/README.md:3`, `research/b45-real-project-scenarios/source-inventory.md:19-35`, and `research/b45-real-project-scenarios/scenario-candidates.json:27-36` explicitly record no target mutation, source-body copying by default, runtime, browser, provider, git or deploy action.
- The S7 schemas encode evidence boundaries. `research/b45-real-project-scenarios/schemas/fixture-manifest.schema.json:43-73` requires source policy fields such as `target_writes_performed: false` and no absolute paths; `redaction-manifest.schema.json:14-16` and `:51-52` require raw/private forbidden values to remain false.
- The implementation surfaces match the advisory architecture. `.codex/hooks/comment_sufficiency_advisory.py:104-172` returns exit code 0, labels warnings as reviewer signals only, and includes disable/validator-unavailable/too-many-files fallback paths. `plugins/product-agent-os/product_agent_os/tools/comment_sufficiency.py:136-182` also emits `blocking: false` and exits 0.
- Self-learning and automation pathways are candidate-only. `plugins/product-agent-os/product_agent_os/self_learning_candidates.py:116-128` and `:171-209` require `candidate_only`, `cannot_apply`, `auto_apply: disabled`, provider/live eval/target writes not performed, and approval before apply. `plugins/product-agent-os/product_agent_os/automation_policy.py:352-396` blocks activation unless manual stability, owner approval, rollback and absence of active runtime markers are present.
- Product-Agent OS discovery/runtime routing treats Professional Code Authoring as `present_unverified` until current evidence exists. `plugins/product-agent-os/product_agent_os/codex_runtime_runner/routes.py:221-249` requires workflow/checklist evidence and states activation is `present_unverified_until_current_evidence`; `plugins/product-agent-os/product_agent_os/discovery.py:3516-3524` requires coding-standard checklist/workflow evidence and warns detection alone is not proof.

The architecture is correctly biased toward `docs_contract_ready`, `synthetic_green`, fixture-local evidence and explicit `no_go` decisions. I did not find source evidence that S7 claims product/runtime/browser/provider/target mutation readiness.

## Findings

### P0

No P0 architecture blocker found.

The current source packets preserve the no-go and approval boundaries for target mutation, runtime/browser/provider execution, CI/blocker enforcement, git/release/deploy and automation. The architecture does not appear to promote S7 fixture-local evidence into production readiness.

### P1

#### P1-1: Lifecycle marker is stale relative to S7 M28-M35 closure

Evidence:

- `.codex/product-agent-os/lifecycle-state.json:3-6` still records `task_id: B45-PCA-M27` and scope for M27 promotion/no-go.
- `.codex/product-agent-os/lifecycle-state.json:25-31` records completion status `promotion_no_go_keep_advisory_only`, `closure_level: docs_contract_ready`, and M27-specific gaps.
- `.codex/product-agent-os/lifecycle-state.json:33-42` records M27/M26/M24 evidence, not S7 M28-M35 evidence.
- `PLAN.md:35` records S7 M28-M35 as implemented source-owned evidence.
- `PLAN.md:36` requires lifecycle hooks/control-plane sync for non-mechanical work.
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md:488` records M35 as implemented with decision packet and S7 closure.

Impact:

The control-plane source and S7 packets say M28-M35 are closed, but the lifecycle marker still points to the older M27 slice. This weakens lifecycle/closure proof for S7 and can confuse lifecycle hooks or reviewers that rely on `.codex/product-agent-os/lifecycle-state.json` as the active marker.

This does not invalidate S7 source-owned evidence, but it means S7 closure is not cleanly represented in the lifecycle-state surface.

Recommended fix:

Run an owner-approved lifecycle/control-plane sync slice to record the S7/M35 completion marker or explicitly mark the lifecycle-state gap as accepted/handoff-required. This review did not update lifecycle-state because the user allowed only this report write.

#### P1-2: S7 control-plane sync decisions are stronger than the visible root-control-plane proof

Evidence:

- `docs/superpowers/specs/batch45-real-project-decision-packet.json:190-196` records `control_plane_sync_decision` with `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, and source registry as `update_required`.
- `docs/superpowers/specs/batch45-real-project-scorecard.json:295-301` also records update-required decisions for plan/test/evals/runlog/source registry.
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json:245-251` records update-required decisions after M33.
- `RUNLOG.md:150-153` has a compact Batch 45 handoff line for S7, but no detailed S7 lifecycle marker.
- `PLAN.md:35` has the key S7 compact pointer and no-go status.

Impact:

The evidence packets correctly keep detailed evidence source-owned, but their `update_required` language creates a reconciliation obligation. Root files are intentionally compact, yet the source packets do not consistently distinguish "updated as compact pointer" from "handoff_required/not_applicable due root budget." That ambiguity is architectural debt in the control-plane sync trail.

Recommended fix:

For future Batch 45 packets, make the control-plane sync result explicit per root file:

- `updated_compact_pointer`
- `not_applicable_no_scope_change`
- `handoff_required_due_root_budget`
- `blocked_by_user_write_scope`

Do not leave `update_required` in final packets unless an owner will actually update the named file in the same slice.

### P2

#### P2-1: S7 baseline/refactor comparison remains static-heavy and cannot support behavior claims

Evidence:

- `docs/superpowers/specs/batch45-real-project-baseline-results.json:3-6` marks M32 as `fixture_local_analysis_only`.
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json:21-23` accepts gaps for fixture-local comparison only, not target/runtime/provider/browser/git/automation claims.
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json:188-196` records low-churn static comparison outcomes and promotion blocked pending representative evidence or accepted static-only policy.
- `docs/superpowers/specs/batch45-real-project-refactor-comparison.json:200-215` records AST/advisory-style verification evidence, not full target runtime or product behavior.
- `docs/superpowers/specs/batch45-real-project-scorecard.json:239-242` recommends `no_go_for_promotion_keep_fixture_local_static_only`.

Impact:

This is aligned with the current no-go decision, but it is a boundary that future readers can easily overrun. The Test Runner Adapter and behavioral proof boundary are intentionally incomplete. S7 is useful as a scenario harness and scoring scaffold, not as proof that agents produce better real-project code.

Recommended fix:

Keep S7 result labels explicit: `fixture_local_static_only`, `analysis_only`, or `docs_contract_ready`. If M36 proceeds, require exact target labels, disposable boundary, approved commands, rollback, no-private-data proof, and runtime/browser evidence before any behavior claim.

#### P2-2: S7 representativeness is narrow relative to the scenario inventory

Evidence:

- `research/b45-real-project-scenarios/README.md:47-52` lists broader scenario families: myPartners CRM, graph scale, advisor, RAG stack, SOL agent orchestration, SOL frontend/runtime, and skill/plugin loader.
- `research/b45-real-project-scenarios/scenario-candidates.json:570-578` records unsupported claims after M29 and recommends first and second scenarios.
- `PLAN.md:35` records actual S7 fixture-local work for two scenarios: `SOL-AGENT-ORCH-01` and `MP-CRM-CHAT-OPEN-01`.

Impact:

The two selected scenarios are reasonable first coverage, but they do not represent graph-scale, RAG, runtime/browser frontend or integration-heavy behavior. This is not a defect in S7 because M35 is no-go, but it prevents general promotion conclusions.

Recommended fix:

Treat the next slice as scenario selection, not promotion. Choose one high-risk deferred family and define one acceptance question, one target boundary, and one rollback route before any new fixture copy or runtime pilot.

#### P2-3: Installed hook surface can be mistaken for enforcement

Evidence:

- `.codex/hooks.json:39-52` and `.codex/hooks/hooks.json:39-52` configure a PostToolUse hook for `.codex/hooks/comment_sufficiency_advisory.py`.
- `.codex/hooks/comment_sufficiency_advisory.py:104-172` returns 0 for disabled, validator unavailable, too many changed files and advisory warning cases.
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md:473-476` records M25 as local non-blocking advisory and M27 as no-go for promotion.

Impact:

The implementation matches the decision, but the mere presence of hook config can look like an active quality gate to a future reviewer. The architecture currently depends on readers preserving the distinction between "installed local reminder" and "blocking enforcement."

Recommended fix:

Keep every hook-facing artifact explicit: `non_blocking`, `exit_0`, `reviewer_signal_only`, `not_ci_gate`. Any future blocking behavior requires new approval, new eval threshold, rollback, hook-governance update and control-plane sync.

### P3

#### P3-1: Architecture atlas status labels are stale orientation metadata

Evidence:

- `research/batch45-professional-code-authoring-architecture-v2.md:329-332` still labels M30-M33 as planned in the M28 decision record area.
- `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md:477-488` records M28-M35 as implemented through S7 closure.
- `PLAN.md:35` records S7 implemented source-owned evidence and no-go decision.

Impact:

This does not affect the source-of-truth status because `PLAN.md`, Track 11 and decision packets are stronger sources. It can still confuse readers because the architecture atlas is one of the first S7 orientation artifacts.

Recommended fix:

In a future docs cleanup, either update the atlas status labels or add a dated note that the M28 atlas is an orientation artifact and later M29-M35 status lives in Track 11 and source packets.

#### P3-2: Local workflow and packaged workflow copies create drift risk

Evidence:

- `.codex/workflows/coding-standards.md` is the local active workflow evidence for this workspace.
- `plugins/product-agent-os/assets/templates/workflows/coding-standards.md:15-17` and `:77-81` define the packaged template copy and evidence ceiling.
- `plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md:9-11` defines the packaged checklist as task-level evidence, not a replacement for control-plane/review.

Impact:

Having local active workflow files and packaged template copies is expected for Product-Agent OS, but it raises drift risk. For Batch 45 specifically, drift could alter what future agents think Professional Code Authoring requires.

Recommended fix:

Keep local workflow as the active source in this workspace and treat packaged copies as distribution templates. Future changes should cite which layer changed and whether a cache/package refresh is in scope.

## Architecture debt

- Lifecycle state does not reflect S7 closure; current active marker remains M27.
- Control-plane sync fields in source packets use `update_required` where final state sometimes appears to be compact root pointer, accepted root-budget gap, or handoff-required.
- S7 scorecard is static/fixture-local by design; runtime/browser/product-behavior proof remains absent.
- Scenario coverage is intentionally narrow and not representative enough for broad Professional Code Authoring promotion.
- Hook configuration exists locally, but the architecture relies on consistent language to prevent confusion between advisory and enforcement.
- Architecture atlas status labels lag behind Track 11 and source packets.
- Workflow/checklist copies exist in both local `.codex/` and packaged template surfaces; ownership and drift rules should stay explicit.

## Recommended fixes

1. Create an owner-approved lifecycle sync slice for S7/M35:
   - update or supersede `.codex/product-agent-os/lifecycle-state.json`;
   - record `task_id`, `closure_level`, completion gaps and evidence pointers for M28-M35;
   - keep M35 decision as no-go/advisory-only.

2. Normalize control-plane sync vocabulary in future Batch 45 packets:
   - use `updated_compact_pointer`, `not_applicable`, `handoff_required`, or `blocked_by_user_scope`;
   - avoid final `update_required` unless the file is actually updated in that slice.

3. Keep Professional Code Authoring promotion blocked until representative evidence exists:
   - no CI/blocker hook;
   - no active automation;
   - no target mutation;
   - no runtime/browser/provider claim;
   - no release/promotion claim.

4. If M36 proceeds, require a new approval packet before execution:
   - exact target and scenario;
   - disposable or reversible target boundary;
   - commands to run;
   - data/privacy exclusions;
   - rollback/delete path;
   - activation/fallback proof requirements;
   - accepted residual risks.

5. Update stale orientation labels in `research/batch45-professional-code-authoring-architecture-v2.md` in a separate docs-maintenance slice, or add a note pointing readers to Track 11 and M35 decision packet for current state.

## Verification gaps

No tests were run by this reviewer. This is an inspection-only architecture review.

Current evidence gaps that remain after the audit:

- no current-run test evidence from this reviewer;
- no runtime/browser/provider/API/live model proof;
- no target-project build/test/run evidence for S7 fixtures;
- no target mutation proof, by design;
- no CI/blocker hook proof;
- no plugin-cache refresh or distribution proof;
- no git/release/deploy/publish proof;
- no product acceptance proof;
- lifecycle-state not updated for S7 due user write boundary;
- control-plane files not updated by this review due user write boundary.

Code-bearing decision evidence:

- `.codex/workflows/coding-standards.md` and `.codex/artifact-templates/coding-standard-checklist.md` were read as required context because Batch 45 concerns code-authoring policy.
- Applying the checklist is not applicable to this review because no code changes were made and no implementation slice was assigned.

## Approval/runtime boundaries

Allowed in this review:

- read source files and source-owned evidence;
- write only `.codex/product-agent-os/reviews/batch45/agent-01-architecture-lifecycle.md`.

Not approved and not performed:

- code changes;
- docs/source registry/control-plane edits outside this report;
- lifecycle-state update;
- hook changes or hook activation changes;
- target workspace mutation;
- target source copy beyond existing fixtures;
- target commands/build/test/runtime;
- browser automation;
- provider/API/live model calls;
- database access or migration;
- MCP/external writes;
- git branch/stage/commit/push/PR;
- release/deploy/publish;
- active automation.

Control-plane sync decision for this review:

- `REQUIREMENTS.md`: `not_applicable_no_scope_change`
- `PLAN.md`: `handoff_required_not_written_by_reviewer_scope`
- `TEST.md`: `not_applicable_no_new_verification_route`
- `EVALS.md`: `not_applicable_no_eval_threshold_change`
- `RUNLOG.md`: `handoff_required_not_written_by_reviewer_scope`
- `prod_test.md`: `not_applicable_batch39_surface`
- `.codex/product-agent-os/lifecycle-state.json`: `handoff_required_not_written_by_reviewer_scope`; stale M27 marker reported as P1

Rollback for this review:

- delete only this report file if the review artifact must be removed.
- no other project state was intentionally changed.

## Confidence

Confidence: medium-high.

Reasons:

- The architecture evidence is consistent across `PLAN.md`, Track 11, S7 research artifacts, decision packets, hooks, candidate-only policy and automation policy.
- The main lifecycle/control-plane gaps are visible and bounded.
- This was read-only inspection; no tests, runtime/browser checks or live/provider calls were run, so confidence does not extend to behavioral execution claims.

## Handoff

Architectural decision: Batch 45 Professional Code Authoring / S7 currently fits the Product-Agent OS control-plane architecture as advisory/source-owned/fixture-local evidence with no-go promotion. The main correction needed is lifecycle/control-plane synchronization, not a rewrite.

Owned artifact from this review:

- `.codex/product-agent-os/reviews/batch45/agent-01-architecture-lifecycle.md`

Forbidden files for this review:

- all code files
- all root control-plane files except read-only inspection
- docs/source registry
- git state
- hooks
- runtime/target workspaces

Assumptions:

- Source packets and Track 11 are current enough for architecture review.
- No hidden runtime execution occurred outside the inspected source evidence.
- The stale lifecycle marker is a sync gap, not evidence that S7 work did not occur.

Recommended next role:

- Product-Agent OS owner or implementation planner for a narrow lifecycle/control-plane sync slice.
- Docs maintainer only if the owner chooses to clean stale architecture atlas labels or compact source-registry pointers.

Completion Brief:

- Done: read-only architecture audit performed and report written.
- Verification: inspection-only; no tests run.
- Closure level: `docs_contract_ready`.
- Gaps: lifecycle-state not updated, control-plane files not updated, no runtime/browser/provider/target/git/release proof.
