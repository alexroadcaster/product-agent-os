# Batch 45 Quality Retest - Security / Privacy / Approval Boundary

Source status: local read-only review artifact for repeat quality/refactor testing.

## Scope

This review covers the security, privacy, target-isolation and approval-boundary conditions that must hold before repeating Batch 45 quality/refactor testing after `B45-PCA-M37-A01`.

Allowed work for this review:

- read the requested local source packets, control-plane files and prior Batch 45 review/remediation reports;
- write this report only;
- do not run external actions, browser automation, provider/live API calls, target commands, git actions, releases, deployments or automations.

Lifecycle note: `.codex/config.toml` routes Task Brief / Completion Brief through `.codex/workflows/task-plan-lifecycle.md` and control-plane sync through `.codex/workflows/control-plane-sync.md`. The visible Task Brief was shown in chat. `.codex/product-agent-os/lifecycle-state.json` currently points to another parallel Batch 45 quality-retest review (`B45-QUALITY-RETEST-ARCH-01`), so this review did not overwrite that shared marker.

## Sources Read

- `docs/superpowers/specs/batch45-review-remediation-summary.json`
- `docs/superpowers/specs/batch45-real-project-decision-packet.json`
- `docs/superpowers/specs/batch45-real-project-scorecard.json`
- `PLAN.md`
- `EVALS.md`
- `TEST.md`
- `AGENTS.md`
- `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md`
- `.codex/product-agent-os/reviews/batch45/remediation-agent-04-code-repair.md`
- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `research/b45-real-project-scenarios/source-policy.md`
- `research/b45-real-project-scenarios/source-inventory.md`
- `research/b45-real-project-scenarios/rereview-2026-06-30.md`
- selected Batch 45 fixture `redaction-manifest.json` files for SOL and myPartners.

## Findings

### P0

No P0 findings for a local-only repeat quality/refactor retest.

### P1

#### P1-01: Runtime/browser/provider/target retesting is blocked until a fresh approval packet exists

Evidence:

- `docs/superpowers/specs/batch45-real-project-decision-packet.json:12` lists target mutation, target command execution, runtime launch, browser automation, provider/live API call, database access, git, release/deploy/publish, CI/blocker enforcement and automation activation as not approved.
- `docs/superpowers/specs/batch45-real-project-decision-packet.json:145-151` reserves `B45-PCA-M36` as optional approval-required work and requires target/disposable boundary, rollback/delete path, data/privacy boundary and provider/live API boundary.
- `docs/superpowers/specs/batch45-real-project-scorecard.json:6` classifies M34 as `fixture_local_scorecard_only`.
- `PLAN.md:35` says S7/M37 remains fixture-local/source-only/local-advisory-hardening evidence and forbids target commands, target mutation, runtime/browser, providers/live APIs, databases, git, deploy, publish and automation without fresh exact approval.
- `AGENTS.md:56` and `AGENTS.md:65` require exact approval before live servers, browser automation, provider/live calls, target mutation, git/external surfaces and runtime/browser/provider/git/external real-project surfaces.

Impact:

Repeat testing may not cross into runtime, browser, provider/live eval, database, target workspace, git/release/deploy or automation behavior by implication. Those surfaces require an explicit `B45-PCA-M36`-style approval packet before execution.

Required action:

Keep repeat retesting local-only unless the owner approves a packet that names the target, commands/actions, data/privacy boundary, provider/live API boundary, evidence artifacts, rollback/delete path and stop conditions.

### P2

#### P2-01: Public/team reuse is blocked until residual absolute-path evidence is cleaned or clearly labeled local-only

Evidence:

- Prior security review `agent-05-security-privacy-approvals.md:68-85` found retained absolute user-specific paths in earlier hook evidence.
- Current scoped scan still finds those paths in prior review text and old Batch 45 evidence, including `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json:57` and `:93`.
- `AGENTS.md:105` forbids secrets, private customer data, raw private chat logs and absolute user-specific paths in templates, fixtures and generated examples.
- `EVALS.md:33` says secrets, private data, raw prompts/traces and absolute user-specific paths are not eval fixtures, examples or templates.
- `remediation-agent-04-code-repair.md:14` records current hook remediation with `workspace_ref` instead of raw absolute path output.

Impact:

This does not block local-only retesting, because M37 appears to have repaired the current hook-output path. It does block public/team sharing, broad report reuse or promotion claims until older retained evidence is either redacted, excluded, or labeled as local-only internal evidence.

Required action:

For repeat retest artifacts, use repository-relative paths, `target_id`, `target_label`, digests, counts and `<workspace>` / `<tempdir>` placeholders only. Do not copy old absolute-path snippets into new scorecards or review packets.

#### P2-02: Raw source/log/private-data restrictions must remain hard gates for any fixture refresh

Evidence:

- `research/b45-real-project-scenarios/source-policy.md:48-49` forbids secrets, credentials, private data, raw chats, raw messages, raw prompts, provider responses, customer/user data and private graph payloads.
- `research/b45-real-project-scenarios/source-policy.md:70-72` forbids absolute user-specific roots and requires target identity through `target_id` / `target_label`.
- `research/b45-real-project-scenarios/source-policy.md:100` forbids original secret values, raw private text, raw prompts, raw provider responses and raw customer/user data in redaction manifests.
- `research/b45-real-project-scenarios/source-policy.md:167-169` forbids raw denylist match lines containing values, raw source excerpts from private files and screenshots/videos/traces of private data.
- SOL and myPartners fixture `redaction-manifest.json:9` both record `raw_private_data_stored: false`.

Impact:

Any repeated quality/refactor test that refreshes fixtures or copies new target material must stop before private/raw content enters `codex_docs`. Static summaries are allowed only when they preserve metadata-only boundaries.

Required action:

Keep fixture refreshes out of scope unless a new packet names the selected files, allowed file classes, denylist result, redaction status, reviewer, target read-only proof and deletion path.

#### P2-03: Lifecycle marker contention is an audit gap, not a retest blocker

Evidence:

- `.codex/product-agent-os/lifecycle-state.json` currently points to `B45-QUALITY-RETEST-ARCH-01`, not this security/privacy report.
- `.codex/workflows/task-plan-lifecycle.md` requires visible Task Brief and marker state before mutating Product-Agent OS execution.
- `.codex/workflows/control-plane-sync.md` requires a before-close control-plane sync decision.

Impact:

The shared marker appears to be used by parallel Batch 45 quality-retest reviewers. Overwriting it would risk clobbering a sibling handoff. This report records the contention as an accepted local review gap.

Required action:

Before any future mutating retest step, use a per-task lifecycle marker strategy or serialize the marker update. Do not use the current marker as proof that this specific review had an isolated lifecycle state.

### P3

#### P3-01: Synthetic privacy canaries remain useful but need explicit allowlisting in future scans

Evidence:

- Prior review `agent-05-security-privacy-approvals.md:130-148` found synthetic privacy canaries in the myPartners fixture and did not classify them as raw private leakage.
- SOL and myPartners redaction manifests both state `raw_private_data_stored: false`.

Impact:

Canary strings can create scanner noise during repeat testing. This is not a blocker if the test remains local and the manifest records the strings as synthetic.

Required action:

Add or preserve a canary inventory when privacy-looking strings are intentionally present. Prefer neutral tokens such as `PRIVACY_CANARY_RAW_MESSAGE` for new fixtures.

## Data Exposure Status

- No new high-confidence secret, credential, private key, provider response, database dump, raw private log, raw private chat, HAR, screenshot or trace exposure was identified in the scoped review.
- Residual absolute-path evidence exists in older Batch 45 review/summary artifacts. Treat it as local-only internal evidence unless redacted.
- Current remediation claims `workspace_ref` path redaction for the hook/validator path, but this review did not rerun tests or hooks.
- Fixture manifests state `raw_private_data_stored: false`; fixture refresh remains approval-gated.

## Approval Boundary Status

Allowed local-only repeat path:

- use existing sanitized fixture packs and source-owned Batch 45 packets;
- run static/local checks only if separately requested in the same local workspace;
- write new evidence under `codex_docs` source-owned paths;
- retain only relative paths, target labels, counts, digests, summary metrics and redacted diagnostics;
- keep M25/M37 advisory behavior non-blocking and reversible;
- keep claims at `fixture-local`, `source-only`, `local-advisory-hardening`, or `inspection-only`.

Forbidden without fresh exact approval:

- target workspace mutation or target command execution;
- runtime launch, live server, browser automation or screenshots/traces;
- provider/live API/model calls or live eval reruns;
- database access, production/local private data access or embedding private content;
- git branch/stage/commit/push/PR, CI/blocker enforcement, release, deploy, publish;
- hook activation in target projects, automation activation, schedules or external workflows;
- broad secret scans, broad link scans, raw report retention or external writes beyond the named local artifact.

## Minimal Safe Packet For Repeat Quality/Refactor Testing

Use this packet before any repeat test that goes beyond reading existing packets:

```yaml
task_id: B45-QUALITY-RETEST-<id>
objective: repeat quality/refactor test without expanding evidence claims
target_scope:
  mode: existing_sanitized_fixture_only | fixture_refresh | disposable_runtime_browser_pilot
  target_id: <stable id>
  target_label: <human label>
  target_workspace_mutation: false
  target_commands: []  # required explicit list if mode is not existing_sanitized_fixture_only
data_boundary:
  raw_private_data_allowed: false
  raw_source_body_copy_allowed: false
  absolute_paths_allowed: false
  provider_live_response_capture_allowed: false
  allowed_evidence: [relative_paths, target_labels, counts, digests, redacted_diagnostics, summary_metrics]
redaction:
  denylist_scan_scope: path_only_or_approved_file_set
  redaction_manifest_required: true
  synthetic_canary_inventory_required: true
approval_surfaces:
  runtime_browser: approval_required
  provider_live_api: approval_required
  database_or_private_data: approval_required
  target_mutation: approval_required
  git_release_deploy_publish: approval_required
  hooks_automation_activation: approval_required
evidence_artifacts:
  output_dir: codex_docs_source_owned_path_only
  no_raw_logs: true
  no_screenshots_or_traces_without_approval: true
rollback_delete_path:
  fixture_outputs: <paths to delete>
  target_workspace: no_change_expected
stop_conditions:
  - secret_or_private_data_detected
  - raw_source_body_required_to_proceed
  - command_would_touch_target_workspace
  - provider_or_browser_or_runtime_needed_without_approval
  - unsupported_behavior_or_readiness_claim_would_be_needed
```

## Blockers

- `runtime/browser/provider/target` retest: blocked until `B45-PCA-M36` or equivalent approval packet exists.
- Public/team promotion of Batch 45 evidence: blocked until residual absolute-path evidence is redacted or labeled local-only and excluded from public/team artifacts.
- Target fixture refresh: blocked until a source-copy/redaction packet names files, denylist scope, reviewer and deletion path.
- CI/blocker promotion: blocked by M27/M35 no-go and M34/M37 claim ceilings.
- Release/deploy/publish/readiness claim: blocked; no current evidence supports it.

## Control-Plane Sync Decision

- `REQUIREMENTS.md`: `not_applicable`; scope and acceptance did not change.
- `PLAN.md`: `not_applicable_for_direct_edit`; existing `PLAN.md:35` already carries the Batch 45 S7/M37 no-go and approval boundary.
- `TEST.md`: `handoff_required_if_repeat_tests_are_scheduled`; add the minimal safe packet checks only when a repeat test is actually scheduled.
- `EVALS.md`: `not_applicable_for_direct_edit`; existing eval ceilings already reject unsupported runtime/product/release claims.
- `RUNLOG.md`: `handoff_required`; detailed evidence belongs in this source-owned report and root `RUNLOG.md` is budget-sensitive.
- `prod_test.md`: `not_applicable`.

## Commands Run

Read-only/local commands:

- `Get-Content` for required Batch 45 packets, control-plane files, lifecycle workflows and prior review/remediation reports.
- `Select-String` over required files and related source-policy artifacts for approval, privacy, target isolation, raw source/log and claim-boundary terms.
- Scoped `rg -n -F` searches for absolute local path markers and raw/private markers in Batch 45/source-policy paths.
- `Get-ChildItem` to list existing Batch 45 review artifacts.

No tests, hooks, external scans, browser automation, provider/live API calls, target commands, git actions, release/deploy/publish steps or automations were run.

## Residual Risks

- This was not a broad secret scan.
- Current hook redaction was accepted from `remediation-agent-04-code-repair.md`; it was not re-executed in this review.
- Shared lifecycle marker contention remains unresolved for parallel Batch 45 quality-retest reviewers.
- Local-only repeat testing can still produce misleading confidence if scorecards average over missing runtime/browser/provider proof; keep blockers explicit.

## Next Role

Next role: `Eval/Test Engineer` only for local fixture/static repeat-test planning. Route to `Release Operator` or runtime/browser pilot planner only if the owner explicitly requests `B45-PCA-M36` approval-packet work.
