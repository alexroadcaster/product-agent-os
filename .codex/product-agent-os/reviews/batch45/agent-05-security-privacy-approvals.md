# Batch 45 Security / Privacy / Approval-Boundary Review

Source status: local independent read-only review artifact.

## Scope

Review focus:

- approval boundaries and overreach in Batch 45 claims;
- privacy/sanitization and raw source/log retention;
- hook and automation safety;
- fixture redaction and retained test artifacts;
- supply-chain/runtime claim gaps before any promotion.

Allowed action boundary for this review:

- read scoped local artifacts only;
- no broad secret scan;
- no browser automation;
- no provider/live API calls;
- no target commands;
- no git actions;
- no automations;
- only write this report:
  `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md`.

Lifecycle note: `.codex/config.toml` routes Task Brief / Completion Brief through `.codex/workflows/task-plan-lifecycle.md` and control-plane sync through `.codex/workflows/control-plane-sync.md`. The visible Task Brief was shown in chat. `.codex/product-agent-os/lifecycle-state.json` still points to earlier `B45-PCA-M27`; it was not updated because the current request allowed only this markdown report as a write.

## Sources read

- `AGENTS.md`
- `PLAN.md`
- `TEST.md`
- `.codex/config.toml`
- `.codex/workflows/task-plan-lifecycle.md`
- `.codex/workflows/control-plane-sync.md`
- `.codex/product-agent-os/lifecycle-state.json`
- `.codex/hooks.json`
- `.codex/hooks/comment_sufficiency_advisory.py`
- `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py`
- `research/b45-real-project-scenarios/source-policy.md`
- `research/b45-real-project-scenarios/fixtures/sol/SOL-AGENT-ORCH-01/{scenario-manifest.json,fixture-manifest.json,redaction-manifest.json}`
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/{scenario-manifest.json,fixture-manifest.json,redaction-manifest.json}`
- scoped `docs/superpowers/specs/batch45-*.json`, with detailed reads of:
  - `batch45-comment-sufficiency-advisory-wiring-summary.json`
  - `batch45-comment-policy-promotion-decision.json`
  - `batch45-real-project-decision-packet.json`

Skill/reference context:

- `security-review`
- `security-best-practices`

Memory was used only as orientation to find current Batch 45 source packets; all status claims below are based on current files and commands from this review.

## Findings

### P0

No P0 findings.

### P1

No P1 findings.

### P2

#### P2-01: Retained Batch 45 hook evidence stores absolute user-specific local paths

Evidence:

- `AGENTS.md:105` says template files, fixtures, and generated examples must not contain absolute user-specific paths.
- `research/b45-real-project-scenarios/source-policy.md:68-70` requires repository-relative manifest paths and forbids absolute user-specific roots in fixtures.
- `.codex/hooks/comment_sufficiency_advisory.py:111-115` emits `"workspace_root": str(root)` in hook JSON.
- `.codex/hooks/comment_sufficiency_advisory.py:160-161` emits scanned paths and `validator_source`.
- `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:111-115` and `:160-161` mirror the same behavior in the packaged template.
- `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json:16`, `:43-44`, `:57`, and `:92-93` retain `C:\Users\user\Desktop\project\codex_docs`, `C:\Users\user\AppData\Local\Temp\...`, and `C:\Python313\python.exe` in command/output evidence.

Impact:

This is not a secret leak by itself, but it is a privacy and reproducibility gap in retained artifacts. It exposes machine/user-specific paths and makes future reports easier to accidentally publish with local identifiers.

Recommendation:

Before promotion or reuse in public/team artifacts, normalize hook output and retained evidence to workspace-relative paths, stable labels, or redacted placeholders such as `<workspace>`, `<tempdir>`, and `<python>`. Add a focused regression check that `comment_sufficiency_advisory.py` output and `batch45-*.json` retained excerpts do not contain drive roots, `C:\Users\`, `AppData`, or absolute interpreter paths unless explicitly marked as local-only internal evidence.

#### P2-02: Packaged advisory hook can import validator code from the target workspace before the packaged source

Evidence:

- `.codex/hooks.json:39-50` wires `comment_sufficiency_advisory.py` as a `PostToolUse` hook.
- `.codex/hooks/comment_sufficiency_advisory.py:13` defines `B45_COMMENT_ADVISORY_ROOT`.
- `.codex/hooks/comment_sufficiency_advisory.py:19` accepts that environment override as the workspace root.
- `.codex/hooks/comment_sufficiency_advisory.py:46-48` searches `repo_root/plugins/product-agent-os/scripts` before the script repo root.
- `.codex/hooks/comment_sufficiency_advisory.py:53-55` inserts that directory into `sys.path` and imports `product_agent_os.comment_sufficiency`.
- The packaged template at `plugins/product-agent-os/assets/templates/hooks/comment_sufficiency_advisory.py:13`, `:19`, `:46-55` has the same behavior.
- `AGENTS.md:103` says packaged hooks are staged target-project assets and target-project hook activation requires explicit approval.

Impact:

In the current trusted `codex_docs` workspace this is bounded by local trust. For packaged/target hook promotion, however, the hook command in `hooks.json` does not fully describe the executable code path: a target workspace can supply the imported validator module under `plugins/product-agent-os/scripts`. That is a supply-chain/approval-boundary gap because approving the hook file may not be enough to understand all code that runs on `PostToolUse`.

Recommendation:

Before any target-project hook activation or broader promotion, pin the validator source to the packaged hook bundle, require a hash/allowlist for workspace-local validator imports, or fail open when the validator source is not the expected Product-Agent OS package path. Also add a negative test proving `B45_COMMENT_ADVISORY_ROOT` cannot redirect the hook into an unreviewed validator source without an explicit trusted-mode flag.

### P3

#### P3-01: `runtime_enabled_local` wording can be misread as stronger runtime proof than Batch 45 supports

Evidence:

- `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json:10` uses `"closure_level": "runtime_enabled_local"`.
- The same packet records `blocker_enforcement_enabled: false`, `browser_automation_used: false`, `ci_workflow_created: false`, `provider_or_model_called: false`, and `target_workspace_mutated: false` at `:3-8`.
- `PLAN.md:34` and `PLAN.md:65` preserve Batch 45 as advisory/no-go: no real AI-agent behavior improvement, no CI/blocker promotion, no browser/runtime proof, no plugin-cache refresh, no target mutation, and future provider/model reruns require exact approval.
- `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json:64` lists unsupported promotion/runtime/product claims.

Impact:

The local advisory did run, so this is not false evidence. The wording is still easy to overread outside the packet context as product/runtime proof rather than local hook-runtime proof.

Recommendation:

Use a narrower closure label in future packets and dashboards, for example `local_hook_advisory_enabled_non_blocking`, or always display `runtime_enabled_local` beside the no-go unsupported-claims list.

#### P3-02: Synthetic privacy canaries in fixtures are intentional but noisy for future privacy scans

Evidence:

- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/redaction-manifest.json:9` says `raw_private_data_stored` is `false`.
- The same manifest at `:13` explicitly notes synthetic test literals may be present.
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/tests/frontend/tests/contracts/crm-model.test.ts:290` includes `"Raw private message from Bob"` as a negative-rendering canary.
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/tests/frontend/tests/e2e/crm.spec.ts:1021`, `:1155`, `:1252`, `:1269`, `:1310`, and `:1325` assert that `"Raw private sentence from Beeper"` is hidden.
- `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/tests/server/tests/test_contacts_messages.py:91` and `:102` include `deleted private text` and `tombstoned private text`.

Impact:

These look like deliberate synthetic privacy canaries, not confirmed private-data leakage. The risk is future scanner/report noise or accidental misclassification as raw private traces.

Recommendation:

Add a fixture canary registry or manifest field that lists the exact synthetic canary strings and their purpose. Prefer neutral tokens such as `PRIVACY_CANARY_RAW_MESSAGE` in future copied fixtures so denylist tools can distinguish intentional synthetic privacy assertions from real private text.

## Privacy/sanitization gaps

- No high-confidence secret, credential, private key, raw provider response, database, log, HAR, screenshot, or Playwright trace retention was found in the scoped artifacts read.
- The main privacy gap is retained absolute local path evidence in `batch45-comment-sufficiency-advisory-wiring-summary.json` and hook JSON output.
- The myPartners fixture has synthetic privacy canaries. Current manifests acknowledge them and state `raw_private_data_stored: false`, but future scans need an allowlisted canary inventory to avoid false escalations.
- Fixture manifests for SOL and myPartners record `absolute_paths_stored: false`, `target_commands_run: []`, and unsupported runtime/browser/provider claims; those boundaries look consistent with the source policy.

## Approval-boundary risks

- Current Batch 45 promotion claims are conservative overall: M27 and M35 keep advisory-only/no-go, reject CI/blocker promotion, reject target apply, and keep runtime/browser/provider/git/deploy/automation approval-required.
- The hook runtime path is the main approval-boundary risk: `hooks.json` names a hook script, but the script can dynamically import validator code from the workspace root before the packaged source.
- `B45_COMMENT_ADVISORY_ROOT` is useful for tests, but before promotion it needs an explicit trust model or negative test so it cannot silently widen the review boundary.
- `PreToolUse` exists in `.codex/hooks.json`, but this review did not execute hooks or broaden into hook activation tests. Existing policy still says target-project hooks require explicit approval.

## Recommended safeguards

1. Redact absolute local paths from hook JSON output and retained Batch 45 evidence.
2. Add a focused no-absolute-path regression over `docs/superpowers/specs/batch45-*.json` and hook output.
3. Pin or allowlist the validator import path for packaged hooks before target-project activation.
4. Add a test that a malicious/unexpected `repo_root/plugins/product-agent-os/scripts/product_agent_os/comment_sufficiency.py` is not imported by default.
5. Keep `comment_sufficiency_advisory.py` non-blocking unless a future owner-approved behavior eval reverses the M27/M35 no-go decisions.
6. Add a fixture canary manifest for synthetic strings that intentionally look like private data.
7. Keep future runtime/browser/provider or disposable-target pilots behind a fresh approval packet naming target, exact commands/actions, rollback/delete path, data boundary, evidence artifacts, and stop conditions.

## Checks to run before promotion

Recommended promotion-gate checks:

- focused path-leak scan:
  `rg -n --glob 'batch45-*.json' 'C:\\Users\\|AppData|C:\\Python|workspace_root|validator_source' docs/superpowers/specs`
- hook-output privacy regression proving no absolute paths are emitted by default;
- hook import-source regression proving the packaged validator or an explicitly allowlisted validator is used;
- fixture canary validation proving synthetic privacy canaries are declared in manifests;
- existing focused hook/comment tests:
  `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v`
- docs/control-plane checks when artifacts change:
  `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
  `python tools\check_docs.py`
  `git diff --check`

Do not run broad secret scans, browser automation, provider/live API calls, target commands, git actions, or automation activation unless a later approval explicitly expands the scope.

## Commands run

Read-only commands:

- `Get-Content` for the two requested security skills.
- `Select-String` over memory registry for Batch 45 orientation.
- `Get-Content` for `.codex/config.toml`, lifecycle/control-plane workflows, lifecycle state, hooks config, hook scripts, source policy, selected Batch 45 JSON packets, and fixture manifests.
- `Get-ChildItem` to enumerate scoped Batch 45 manifests and `docs/superpowers/specs/batch45-*.json`.
- Scoped `rg -n` searches over the requested files and Batch 45 artifacts for approval, privacy, hook, path, raw-data, and supply-chain terms.
- `Test-Path` and `Get-ChildItem` for the report directory.

No commands executed hooks, tests, browser automation, provider/live APIs, target commands, git actions, broad secret scans, or automations.

## Control-plane sync decision

- `REQUIREMENTS.md`: `not_applicable`; this review did not change scope or acceptance.
- `PLAN.md`: `handoff_required`; no direct update allowed by the user, but future Batch 45 promotion planning should include the P2 safeguards above.
- `TEST.md`: `handoff_required`; no direct update allowed, but promotion checks should add no-absolute-path and hook import-source regressions.
- `EVALS.md`: `not_applicable`; no eval rubric changed in this review.
- `RUNLOG.md`: `handoff_required`; no direct update allowed, and detailed evidence belongs in this report.
- `prod_test.md`: `not_applicable`.
- `RUNLOG.md` overflow decision: `not_checked`; root control-plane mutation was outside this review's write scope.

## Confidence

Confidence: medium-high for scoped Batch 45 approval/privacy/hook findings.

Limits:

- This was not a broad secret scan.
- This did not execute hooks, tests, target commands, browser automation, provider/live APIs, git actions, or automations.
- Findings are limited to the sources named by the user plus directly referenced lifecycle/config artifacts.
